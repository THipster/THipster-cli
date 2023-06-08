from setuptools import setup, find_packages

__version__ = '0.1.0'

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='thipstercli',
    version=__version__,
    description='',
    long_description=long_description,
    authors=[
        {"name": "rcattin", "email": "rcattin@ippon.fr"},
        {"name": "gsuquet", "email": "gsuquet@ippon.fr"},
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python :: 3.11',
    ],
    download_url='https://github.com/THipster/THipster-cli.git',
    url='https://github.com/THipster/THipster-cli',
    install_requires=required,
    packages=find_packages(
        exclude=['ci'],
    ),
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
    entry_points={
        'console_scripts': [
            'thipster = thipstercli.cli:app',
        ],
    },
)
