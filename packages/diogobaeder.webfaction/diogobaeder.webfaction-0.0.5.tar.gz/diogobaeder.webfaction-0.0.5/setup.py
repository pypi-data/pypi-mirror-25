from setuptools import setup, find_packages


setup(
    name='diogobaeder.webfaction',
    use_scm_version=True,
    description="Tools to help with deploying to Webfaction",
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='diogobaeder webfaction python django',
    author='Diogo Baeder',
    author_email='diogobaeder@yahoo.com.br',
    url='https://github.com/diogobaeder/diogobaeder.webfaction',
    license='BSD 2-Clause License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'cryptography',
        'Fabric3',
        'keyring',
        'keyrings.alt',
        'SecretStorage',
        'setuptools_scm',
        'wfcli',
    ],
    namespace_packages=['diogobaeder'],
    entry_points='',
)
