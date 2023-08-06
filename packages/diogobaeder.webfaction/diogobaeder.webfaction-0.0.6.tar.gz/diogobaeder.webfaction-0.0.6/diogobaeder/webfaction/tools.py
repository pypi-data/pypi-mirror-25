from io import StringIO
from os.path import join
from uuid import uuid4

from fabric import colors
from fabric.api import (
    cd, env, get, prefix, put, run, shell_env, warn_only
)
from fabric.contrib.files import upload_template, exists
from wfcli import WebFactionAPI, WebfactionWebsiteToSsl


def info(*texts):
    text = ' '.join(texts)
    print(colors.magenta(text))


class Caller:
    def __init__(self, server, session_id, method_name):
        self.server = server
        self.session_id = session_id
        self.method_name = method_name

    def __call__(self, *args):
        info('xmlrpc:', self.method_name)
        method = getattr(self.server, self.method_name)
        return method(self.session_id, *args)


class WebFactionClient(WebFactionAPI):
    def __getattr__(self, method_name):
        self.connect()
        return Caller(self.server, self.session_id, method_name)

    def command(self, command):
        print(command)
        return self.system(command)


class Maestro:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> WebFactionClient:
        client = WebFactionClient(
            username=env.user, password=env.password)
        client.connect()

        return client

    @property
    def domain(self):
        return Domain(self.client)

    @property
    def db(self):
        return Database(self.client)

    @property
    def apps(self):
        return Applications(self.client)

    @property
    def ssh(self):
        return SSH(self.client)

    @property
    def git(self):
        return Git(self.client)

    @property
    def project(self):
        return Project(self.client)

    @property
    def cache(self):
        return Cache(self.client)

    @property
    def website(self):
        return Website(self.client)


class Component:
    def __init__(self, client: WebFactionClient):
        self.client = client

    def add_on_reboot(self, command):
        self.add_cron('@reboot', command)

    def add_cron(self, when, command):
        cron_command = '{} {}'.format(when, command)
        if cron_command not in run('crontab -l'):
            self.client.create_cronjob(cron_command)

    def is_running(self, program):
        with warn_only():
            result = run('pgrep {}'.format(program))
        if result.failed:
            return False
        return bool(result.strip())

    def all_subdomains(self):
        return [env.project] + self.static_subdomains()

    def static_subdomains(self):
        return [
            '{}{}'.format(env.project, static)
            for static in env.statics
        ]


class Domain(Component):
    def prepare(self):
        self.client.create_domain(env.parent_domain, self.all_subdomains())


class Database(Component):
    def prepare(self):
        if not self._has_user(env.db_user):
            self.client.create_db_user(env.db_user, env.db_pass, env.db_type)
        if not self._has_db(env.db_name):
            self.client.create_db(
                env.db_name, env.db_type, env.db_pass, env.db_user)

    def _has_user(self, user):
        return any(
            db['username'] == user for db in self.client.list_db_users())

    def _has_db(self, name):
        return any(db['name'] == name for db in self.client.list_dbs())


class Applications(Component):
    def prepare(self):
        self.create_app('git', 'git')
        self.prepare_certificate_manager()
        run('mkdir -p {}'.format(join(env.home_dir, 'bin')))
        run('mkdir -p {}'.format(join(env.home_dir, 'tmp')))
        run('easy_install-{} --upgrade pip'.format(env.python_version))
        self.install('virtualenv', 'virtualenvwrapper', 'circus', 'circus-web')
        self.create_app(env.project, 'custom_app_with_port')
        for static in env.statics:
            self.create_static(static)

    def prepare_certificate_manager(self):
        run('mkdir -p ~/src')
        with cd('~/src'):
            run('wget http://www.dest-unreach.org/socat/download/'
                'socat-{}.tar.gz'.format(env.socat_version))
            run('tar xvzf socat-{}.tar.gz'.format(env.socat_version))
            with cd('socat-{}'.format(env.socat_version)):
                run('./configure --prefix={}'.format(env.home_dir))
                run('make')
                run('make install')
        if not exists('~/.acme.sh'):
            run('curl https://get.acme.sh | sh')
        run('~/.acme.sh/acme.sh --upgrade')
        self.add_cron(
            '7 0 * * *',
            '~/.acme.sh/acme.sh --cron --force --home "{}"'.format(
                env.home_dir))

    def create_static(self, static_name):
        path = join(env.project_dir, static_name)
        run('mkdir -p {}'.format(path))
        self.create_app(
            '{}{}'.format(env.project, static_name), 'symlink_static_only',
            path)

    def install(self, *packages):
        run('pip{} install --user -U {}'.format(
            env.python_version, ' '.join(packages)))

    def create_app(self, app_name, app_type, extra_info=''):
        info('creating app', app_name)
        if app_name not in self.client.list_apps():
            return self.client.create_app(
                app_name, app_type, extra_info=extra_info)


class SSH(Component):
    def prepare(self):
        self.create_keys()
        self.ensure_authorized_key()

    def ensure_authorized_key(self):
        info('ensuring authorized key is set')
        with open(env.key_filename, encoding='utf-8') as f:
            key = f.read().strip()

        path = '/tmp/{}'.format(uuid4())
        self.client.write_file(path, key, 'w')
        self.client.command((
            'grep -a "`cat {0}`" ~/.ssh/authorized_keys || '
            'echo "\n`cat {0}`\n" >> ~/.ssh/authorized_keys'
        ).format(path))
        self.client.command('rm {}'.format(path))

    def create_keys(self):
        self.client.command('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
        self.client.command('ssh-keygen -P "" -t rsa -f ~/.ssh/{}-key'.format(
            env.project))
        buffer = StringIO()
        get('~/.ssh/{}-key.pub', buffer)
        public_key = buffer.getvalue()
        info('Make sure you paste the public key in the repo server:')
        print('\n{}\n'.format(public_key))


class Git(Component):
    def prepare(self):
        if not self._has_working_tree():
            self.git(
                'init .',
                'remote add origin {}'.format(env.repository),
            )
        self.fetch_latest()

    def fetch_latest(self):
        self.git(
            'fetch origin',
            'reset --hard origin/master',
        )

    def git(self, *commands):
        with cd(env.project_dir):
            for command in commands:
                run('git {}'.format(command))

    def _has_working_tree(self):
        with cd(env.project_dir), warn_only():
            result = run('test -d .git')
        return not result.failed


class Project(Component):
    def prepare(self):
        if not self._has_virtualenv():
            self._create_virtualenv()

        self.update_files_and_data()
        env.server_port = self.client.list_apps()[env.project]['port']
        upload_template(
            'server.cfg.template', join(env.project_dir, 'server.cfg'), env)

    def update_files_and_data(self):
        with shell_env(TMPDIR='~/tmp'):
            self.env_run('.env/bin/pip install -r requirements.txt')
        settings_module_path = '{}.py'.format(
            env.django_settings_module.replace('.', '/'))
        put(settings_module_path,
            join(env.project_dir, settings_module_path))
        self.manage('migrate')
        self.manage('collectstatic --noinput')
        self.manage('compilemessages')

    def _create_virtualenv(self):
        with cd(env.project_dir):
            run('virtualenv .env')

    def manage(self, command):
        with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
            self.env_run('.env/bin/python manage.py {}'.format(command))

    def env_run(self, command):
        with cd(env.project_dir), prefix('source .env/bin/activate'):
            run(command)

    def _has_virtualenv(self):
        with cd(env.project_dir), warn_only():
            result = run('test -d .env')
        return not result.failed


class Website(Component):
    def prepare(self):
        command = 'cd {} && .env/bin/circusd --daemon server.cfg'.format(
            env.project_dir)
        for d in self.all_subdomains():
            self.create_website(d)

        self.add_on_reboot(command)
        if not self.is_running('circusd'):
            run(command)
        else:
            self.reload_config()

    def reload_config(self):
        with cd(env.project_dir):
            run('circusctl reloadconfig')

    def reload(self):
        with cd(env.project_dir):
            run('circusctl reload')

    def create_website(self, subdomain):
        info('creating website for:', subdomain)
        domain = '{}.{}'.format(subdomain, env.parent_domain)
        websites = [w['name'] for w in self.client.list_websites()]
        if subdomain not in websites:
            self.client.create_website(
                subdomain, env.ip, False, [domain], apps=(
                    [subdomain, '/'],
                ))
            if env.https:
                info('securing domain:', domain)
                ssl = WebfactionWebsiteToSsl(env.hosts[0])
                ssl.secure(domain, False)


class Cache(Component):
    COMMAND = (
        'memcached -d -m 50 -s $HOME/memcached.sock -P $HOME/memcached.pid')

    def prepare(self):
        self.add_on_reboot(self.COMMAND)
        self.start()

    def start(self):
        if not self.is_running('memcached'):
            run(self.COMMAND)
