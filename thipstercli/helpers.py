import sys
import typer
import importlib
from rich import print
from thipstercli.config import state
from importlib.metadata import version as get_version


def error(*args, **kwargs):
    print('[bold][red]Error :[/red][/bold]', *args, file=sys.stderr, **kwargs)
    sys.stderr.flush()
    raise typer.Exit(1)


def print_if_verbose(text: str):
    print(text) if state['verbose'] else None


def print_start_if_verbose(text: str):
    print_if_verbose(f':arrow_forward: {text} ...')


def print_success_if_verbose(text: str):
    print_if_verbose(f'{text} :white_heavy_check_mark:')


def print_package_version(package: str):
    print(f':bookmark: {package} [green]v{get_version(package)}[/green]')


def get_auth_provider_class(provider: str) -> type:
    provider_module = importlib.import_module(
        f'thipster.auth.{provider.lower()}',
    )
    return getattr(provider_module, f'{provider}Auth')
