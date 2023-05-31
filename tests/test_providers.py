from typer.testing import CliRunner
from thipstercli.providers import app

runner = CliRunner()

providers = [
    "google",
]


def test_list_providers():
    result = runner.invoke(app, ["list"])
    for provider in providers:
        assert provider in result.stdout.lower()
