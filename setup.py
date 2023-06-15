from setuptools import setup, find_packages

__version__ = '0.2.0'

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('requirements-dev.txt') as f:
    required_dev = f.read().splitlines()

with open('requirements-doc.txt') as f:
    required_doc = f.read().splitlines()

with open('requirements-test.txt') as f:
    required_test = f.read().splitlines()

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
    extras_require={
        'dev': required_dev,
        'doc': required_doc,
        'test': required_test,
    },
    entry_points={
        'console_scripts': [
            'thipster = thipstercli.cli:app',
        ],
    },
)
