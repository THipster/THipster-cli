from importlib.metadata import version as get_version
from typer.testing import CliRunner
from thipstercli.cli import app
import os

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    version = get_version("thipster-cli")
    assert "THipster-cli" and version in result.stdout


def test_version_thipster():
    result = runner.invoke(app, ["version", "--thipster"])
    version = get_version("thipster-cli")
    assert "THipster-cli" and version in result.stdout
    version = get_version("thipster")
    assert "THipster" and version in result.stdout


def test_run_file():
    os.environ["GOOGLE_CREDENTIALS"] = """{
        "type": "service_account",
        "project_id": "thipster-test",
    }"""
    result = runner.invoke(app, ["-v", "run", "tests/resources/bucket.thips"])
    assert "Running THipster on tests/resources/bucket.thips" in result.stdout

    assert "bucket" in result.stdout

    del os.environ["GOOGLE_CREDENTIALS"]
