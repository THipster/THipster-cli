from importlib.metadata import version as get_version
from typer.testing import CliRunner
from thipstercli.cli import app
import os

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    version = get_version("thipstercli")
    assert result.exit_code == 0
    assert "THipster-cli" and version in result.output


def test_version_thipster():
    result = runner.invoke(app, ["version", "--thipster"])
    version = get_version("thipstercli")
    assert result.exit_code == 0
    assert "THipster-cli" and version in result.output
    version = get_version("thipster")
    assert "THipster" and version in result.output


def test_run_wrong_local_repository():
    result = runner.invoke(
        app, ["run", "tests/resources/bucket.thips", "--local", "wrong_path"],
    )
    assert result.exit_code == 0
    assert "Error: No such file or directory :" in result.output
    assert "wrong_path" in result.output


def test_run_wrong_file_path():
    result = runner.invoke(app, ["run", "wrong_path"])
    assert result.exit_code == 0
    assert "Error: Path not found :" in result.output
    assert "wrong_path" in result.output


def test_run_bucket():
    AUTH_FILE_PATH = "tests/credentials.json"
    auth_file = open(AUTH_FILE_PATH, "w")
    auth_file.write(os.environ["GOOGLE_APPLICATION_CREDENTIALS_CONTENT"])
    auth_file.close()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = AUTH_FILE_PATH

    try:
        result = runner.invoke(
            app, [
                "run", "tests/resources/bucket.thips",
                "-l", "tests/resources/models",
            ],
        )
    finally:
        os.remove(AUTH_FILE_PATH)

    assert result.exit_code == 0
    assert "thipster_cli_test_bucket" in result.output
    assert "Terraform will perform the following actions" in result.output
