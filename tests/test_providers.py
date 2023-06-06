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


def test_info_provider():
    result = runner.invoke(app, ["info", "google"])
    assert "google" in result.stdout.lower()
    assert "help" in result.stdout.lower()


def test_set_provider():
    result = runner.invoke(app, ["set", "google"])
    assert "google" in result.stdout.lower()
    assert "provider set to" in result.stdout.lower()

    result = runner.invoke(app, ["display"])
    assert "google" in result.stdout.lower()
    assert "provider set to" in result.stdout.lower()
