# THipster CLI

CLI tool to interact and use [THipster](https://github.com/THipster/THipster), build with [Typer](https://typer.tiangolo.com/).

THipster is a tool dedicated to simplifying the ordeal associated with writing Terraform files.
It allows users to write infrastructure as code in a simplified format, using either YAML (with JINJA) or the dedicated Thipster DSL.

Written entirely in Python, it leverages the Python CDK for Terraform to create Terraform files and apply them to the chosen provider.


## Technology Stack
Written in Python 3.11, thipster-cli is build using [Typer](https://typer.tiangolo.com/).

## Project Status
THipster-cli is currently in an active development state. If you want to know more, please check the [CHANGELOG](CHANGELOG.md) for more details.

## Dependencies

To use the CLI, you will need to have all the required THipster dependencies installed on your machine. Please refer to the [THipster documentation](https://github.com/THipster/THipster#dependencies) for more details.

## Installation

*Detailed instructions on how to install, configure, and get the project running.
This should be frequently tested to ensure reliability. Alternatively, link to
a separate [INSTALL](INSTALL.md) document.*

## Usage

*Show users how to use the software.
Be specific.
Use appropriate formatting when showing code snippets.*

## How to test the software

To test the CLI, you can run the following command:

```bash
pip install -e .[test]
pytest tests
```

## Known issues

All known issues, bugs, improvements, etc. are tracked as [GitHub issues](https://github.com/THipster/THipster-cli/issues).

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's [Issue Tracker](https://github.com/THipster/THipster-cli/issues).

## Getting involved

To install the project in development mode, run the following command:

```bash
pip install -e .[dev,test]
pre-commit install && pre-commit run --all-files
```

If you would like to be involved in the project feel free to check the [CONTRIBUTING](https://github.com/THipster/THipster-cli/blob/main/CONTRIBUTING.md) file. We will be happy to have you onboard.

## Open source licensing info
1. [LICENSE](https://github.com/THipster/THipster-cli/blob/main/LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
