import typer
from thipstercli import providers
from thipstercli.state import state, init_state
from rich import print
from thipster import Engine as ThipsterEngine
from thipster.repository import GithubRepo, LocalRepo
from thipster.parser import ParserFactory
from thipster.parser.parser_factory import ParserPathNotFound
from thipster.parser.dsl_parser.exceptions import (
    DSLSyntaxException,
    DSLConditionException,
    DSLUnexpectedEOF,
)
from thipster.auth import Google
from thipster.terraform import Terraform
from thipster.terraform.exceptions import CDKException

init_state()
app = typer.Typer(name=state["app_name"], no_args_is_help=True)
app.add_typer(providers.app, name="providers")


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
    print(f"{state['app_name']}")

    if thipster:
        print(
            f":bookmark: THipster [green]v{state['thipster_version']}[/green]",
        )


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

    repo = LocalRepo(local) if local else GithubRepo(state["github_repo"])
    __display_vb("Repo set-up successful! :memo:")

    engine = ThipsterEngine(
        ParserFactory(), repo,
        Google, Terraform(),
    )
    __display_vb("Engine start-up successful! :rocket:")

    __display_vb("Parsing files...")

    try:
        list_dir, tf_plan = engine.run(path)
        print(tf_plan)
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
