import typer
from thipstercli import providers
from importlib.metadata import version as get_version
from rich import print
from thipster.engine.Engine import Engine as ThipsterEngine
from thipster.repository.GithubRepo import GithubRepo
from thipster.repository.LocalRepo import LocalRepo
from thipster.parser.ParserFactory import ParserFactory, ParserPathNotFound
from thipster.parser.dsl_parser.TokenParser import DSLSyntaxException,\
    DSLConditionException, DSLUnexpectedEOF
from thipster.auth.Google import GoogleAuth
from thipster.terraform.CDK import CDK, CDKException

version = get_version("thipstercli")

name = f":bookmark: THipster-cli [green]v{version}[/green]"

app = typer.Typer(name=name, no_args_is_help=True)
app.add_typer(providers.app, name="providers")

state = {
    "verbose": False,
}


@app.callback()
def _callback(
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Prints more information about the execution of the THipster CLI",
    ),
):
    """THipster CLI

    THipster is a tool that allows you to generate Terraform code 
    from a simple DSL or yaml file.
    """
    state["verbose"] = verbose


@app.command("version")
def _version(
    thipster: bool = typer.Option(
        False,
        "--thipster", "-t",
        help="Prints the version of the THipster tool",
    ),
):
    """Prints the version of the THipster CLI
    """
    print(f"{name}")

    if thipster:
        print(f":bookmark: THipster [green]v{get_version('thipster')}[/green]")


@app.command("run")
def _run(
    path: str = typer.Argument(
        ...,
        help="Path to the file or directory to run",
    ),
    local: str = typer.Option(
        None,
        "--local", "-l",
        help="Runs the THipster Tool locally, importing models from the given path",
    ),
):
    """Runs the THipster Tool on the given path
    """
    __display_vb(f"Running THipster on {path}")

    repo = LocalRepo(local) if local else GithubRepo('THipster/models')
    __display_vb("Repo set-up successful! :memo:")

    engine = ThipsterEngine(
        ParserFactory(), repo,
        GoogleAuth, CDK(),
    )
    __display_vb("Engine start-up successful! :rocket:")

    __display_vb("Parsing files...")

    try:
        print(engine.run(path))
        __display_vb("Done! :tada:")
    except ParserPathNotFound as e:
        print(f"[red]Error:[/red] {e.message}")
    except DSLSyntaxException as e:
        print(f"[red]Error:[/red] {repr(e)}")
    except DSLConditionException as e:
        print(f"[red]Error:[/red] {repr(e)}")
    except DSLUnexpectedEOF as e:
        print(f"[red]Error:[/red] {repr(e)}")
    except CDKException as e:
        print(f"[red]Error:[/red] {e.message}")


def __display_vb(text: str):
    print(text) if state["verbose"] else None


if __name__ == "__main__":
    app()
