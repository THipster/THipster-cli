import typer
import os
from thipster import auth

app = typer.Typer(no_args_is_help=True)

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


@app.command("list")
def _list():
    """List all the supported providers
    """
    with os.scandir(os.path.dirname(auth.__file__)) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith(".py") and not \
                    entry.name.startswith("__"):
                print(entry.name[:-3])


if __name__ == "__main__":
    app()
