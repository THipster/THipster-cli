"""THipster CLI."""
import typer
from rich import print
from thipster import Engine as ThipsterEngine
from thipster.auth import Google
from thipster.engine.exceptions import THipsterException
from thipster.parser import ParserFactory
from thipster.repository import GithubRepo, LocalRepo
from thipster.terraform import Terraform

import thipstercli.constants as constants
from thipstercli import providers
from thipstercli.config import init_parameters, state
from thipstercli.display import (
    error,
    print_if_verbose,
    print_package_version,
    print_start_if_verbose,
    print_success_if_verbose,
)

init_parameters()

app = typer.Typer(
    name=state.get(
        'app_name', constants.APP_NAME,
    ), no_args_is_help=True,
)
app.add_typer(providers.app, name='providers')


@app.callback()
def _callback(
    verbose: bool = typer.Option(
        state.get('verbose', constants.VERBOSE),
        '--verbose', '-v',
        help='Prints more information about the execution of the THipster CLI',
    ),
):
    """THipster CLI.

    THipster is a tool that allows you to generate Terraform code
    from a simple DSL or yaml file.
    """
    state['verbose'] = verbose


@app.command('version')
def _version(
    thipster: bool = typer.Option(
        False,
        '--thipster', '-t',
        help='Prints the version of the THipster tool',
    ),
):
    """Print the version of the THipster CLI."""
    print_package_version('thipstercli')

    if thipster:
        print_package_version('thipster')


@app.command('run')
def _run(
    path: str = typer.Argument(
        state.get('input_dir', constants.INPUT_DIR),
        help='Path to the file or directory to run',
    ),
    local: str = typer.Option(
        None,
        '--local', '-l',
        help='Runs the THipster Tool locally, importing models from the given path',
    ),
    repository: str = typer.Option(
        state.get('models_repository', constants.MODELS_REPOSITORY),
        '--repository-name', '-rn',
        help='Runs the THipster Tool using the given model repository',
    ),
    repository_branch: str = typer.Option(
        state.get(
            'models_repository_branch',
            constants.MODELS_REPOSITORY_BRANCH,
        ),
        '--repository-branch', '-rb',
        help='Runs the THipster Tool using the given model repository branch',
    ),
    provider: str = typer.Option(
        None,
        '--provider', '-p',
        help='Runs the THipster Tool using the given provider',
    ),
    apply: bool = typer.Option(
        False,
        '--apply', '-a',
        help='Applies the generated Terraform code',
    ),
):
    """Run the THipster Tool on the given path."""
    print_if_verbose(f'Running THipster on {path}')

    authentification_provider = providers.get_auth_provider_class(
        providers.check_provider_exists(provider),
    ) if provider else Google

    print_if_verbose(
        f'Provider Auth set to [green]{authentification_provider.__name__}[/green]',
    )

    repo = LocalRepo(local) if local else GithubRepo(
        repository,
        repository_branch,
    )
    print_if_verbose('Repo set-up successful! :memo:')

    engine = ThipsterEngine(
        ParserFactory(),
        repo,
        authentification_provider,
        Terraform(),
    )
    print_if_verbose('Engine start-up successful! :rocket:')

    try:
        print_start_if_verbose('Parsing files')
        parsed_file = engine._parse_files(path)
        print_success_if_verbose('Parsing successful!')

        print_start_if_verbose('Retrieving models')
        models = engine._get_models(parsed_file)
        print_success_if_verbose('Models retrieved!')

        print_start_if_verbose('Generating Terraform files')
        engine._generate_tf_files(parsed_file, models)
        print_success_if_verbose('Terraform files generated!')

        print_start_if_verbose('Initializing Terraform')
        engine._init_terraform()
        print_success_if_verbose('Terraform initialized!')

        print_start_if_verbose('Creating Terraform plan')
        print(engine._plan_terraform())

        if apply:
            print("Type 'yes' to apply the changes : ")
            print(engine._apply_terraform())

        print_if_verbose('Done! :tada:')

    except THipsterException as e:
        error(e.message)
    except FileNotFoundError as e:
        error(
            f'No such file or directory : [bold][red]{e.filename}[/red][/bold]',
        )
    except Exception as e:
        error(*e.args)


if __name__ == '__main__':
    app()
