from pathlib import Path
from setuptools import setup, find_packages


def get_extra_requires() -> dict[str, list[str]]:
    extras_require = {}
    for req_file in Path('.').glob('requirements-*.txt'):
        extras_require[
            req_file.stem.removeprefix('requirements-')
        ] = req_file.read_text().splitlines()
    return extras_require


__version__ = '0.2.1'

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='thipstercli',
    version=__version__,
    license='MIT',
    description='CLI interface build with typer, designed to use the thipster package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    authors=[
        {'name': 'rcattin', 'email': 'rcattin@ippon.fr'},
        {'name': 'gsuquet', 'email': 'gsuquet@ippon.fr'},
    ],
    keywords=[
        'thipster',
        'cli',
        'generator',
        'infrastructure as code',
        'iac',
        'terraform',
        'typer',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    download_url='https://github.com/THipster/THipster-cli.git',
    url='https://github.com/THipster/THipster-cli',
    install_requires=required,
    packages=find_packages(
        exclude=['ci'],
    ),
    extras_require=get_extra_requires(),
    entry_points={
        'console_scripts': [
            'thipster = thipstercli.cli:app',
        ],
    },
)
