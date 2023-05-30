from setuptools import setup

__version__ = '0.0.0'

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='thipster-cli',
    version=__version__,
    description='Thipster CLI',
    package_dir={'': 'thipster-cli'},
    install_requires=required,
    extras_require={
        'test': [
            'pytest',
            'pytest-mock',
        ],
        'dev': [
            'pytest',
            'pytest-mock',
            'dagger.io',
            'pre-commit',
        ],
    },
)
