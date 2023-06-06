import typer
import os
import importlib
from rich.panel import Panel
from rich import print
from thipster import auth
from thipstercli.state import state

app = typer.Typer(no_args_is_help=True)


@app.command("list")
def _list():
    """List all the supported providers
    """
    __get_provider_list()
    provider_display = ""
    for provider in state["providers"]:
        provider_display += f"[green]{provider[:-3]}[/green]\n"
    print(Panel(provider_display, title="Providers"))
    __more_info_provider()


@app.command("info")
def info(provider: str):
    """Get information about a provider
    """
    __get_provider_list()
    provider = __check_provider_exists(provider)

    provider_module = importlib.import_module(f"thipster.auth.{provider}")
    provider_description = getattr(provider_module, "description")
    provider_help = getattr(provider_module, "help")
    print(Panel(provider_description, title=provider))
    print(Panel(provider_help, title="Help"))


@app.command("set")
def set(provider: str):
    """Set the provider to use
    """
    __get_provider_list()
    provider = __check_provider_exists(provider)

    provider_module = importlib.import_module(f"thipster.auth.{provider}")
    provider_class = getattr(provider_module, f"{provider}Auth")
    state["provider"] = provider_class

    print(f"Provider set to [green]{provider}[/green]")
    __more_info_provider()


@app.command("display")
def display():
    """Display the current provider
    """
    if state["provider"]:
        print(f"Provider set to [green]{state['provider'].__name__}[/green]")
    else:
        print("No provider set.\nPlease use [bold]thipster providers set <provider>\
[/bold] to set a provider")


def __check_provider_exists(provider: str) -> str:
    """Checks if the given provider exists in the providers list
    """
    if provider.islower():
        provider = provider.capitalize()

    if f"{provider}.py" not in state["providers"]:
        print(f"Provider [red]{provider}[/red] not found. Please use one of the \
following providers:")
        _list()
        raise typer.Exit()

    return provider


def __get_provider_list():
    """Gets the list of providers supported by the thipster package
    """
    if len(state["providers"]) > 0:
        return
    with os.scandir(os.path.dirname(auth.__file__)) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".py") and not \
                    entry.name.startswith("__"):
                state["providers"].append(entry.name)


def __more_info_provider():
    print(
        Panel("For more information about a provider, run: thipster providers info \
<provider>"),
    ) if state["verbose"] else None


if __name__ == "__main__":
    app()
