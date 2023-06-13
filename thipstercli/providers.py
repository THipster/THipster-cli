import typer
import os
from rich.panel import Panel
from rich import print
from thipster import auth
from thipstercli.config import state, update_config_file
from thipstercli.helpers import get_auth_provider_class

app = typer.Typer(no_args_is_help=True)


@app.command('list')
def _list():
    """List all the supported providers
    """
    __get_provider_list()
    provider_display = ''
    for provider in state['providers']:
        provider_display += f'[green]{provider[:-3]}[/green]\n'
    print(Panel(provider_display, title='Providers'))
    __more_info_provider()


@app.command('info')
def info(provider: str):
    """Get information about a provider
    """
    __get_provider_list()
    provider = check_provider_exists(provider)

    provider_class = get_auth_provider_class(provider)
    print(Panel(provider_class.__doc__, title=provider))


@app.command('set')
def set(provider: str):
    """Set the provider to use
    """
    provider = check_provider_exists(provider)

    update_config_file(
        {'auth_provider': provider},
    )

    print(f'Provider set to [green]{provider}[/green]')
    __more_info_provider()


@app.command('display')
def display():
    """Display the current provider
    """
    if state['auth_provider']:
        print(f"Provider set to [green]{state['auth_provider']}[/green]")
    else:
        print('No provider set.\nPlease use [bold]thipster providers set <provider>\
[/bold] to set a provider')


def check_provider_exists(provider: str) -> str:
    """Checks if the given provider exists in the providers list
    """
    __get_provider_list()
    if provider.islower():
        provider = provider.capitalize()

    if f'{provider}.py' not in state['providers']:
        Exception(f'Provider [red]{provider}[/red] not found. Please use one of the \
following providers:')
        _list()
        raise typer.Exit(1)

    return provider


def __get_provider_list():
    """Gets the list of providers supported by the thipster package
    """
    if len(state['providers']) > 0:
        return
    with os.scandir(os.path.dirname(auth.__file__)) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.py') and not \
                    entry.name.startswith('__'):
                provider = entry.name.capitalize() if entry.name.islower() else \
                    entry.name
                state['providers'].append(provider)


def __more_info_provider():
    print(
        Panel('For more information about a provider, run: thipster providers info \
<provider>'),
    ) if state['verbose'] else None


if __name__ == '__main__':
    app()
