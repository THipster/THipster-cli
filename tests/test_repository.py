"""Test the repository subcommand."""
import os

import pytest
from typer import get_app_dir
from typer.testing import CliRunner

import thipstercli.constants as constants
from tests.conftest import get_config_file
from thipstercli.repository import repository_app

runner = CliRunner(mix_stderr=False)


@pytest.fixture
def create_models_directory():
    models_path = os.path.join(get_app_dir(constants.APP_NAME), 'models')
    os.mkdir(models_path)

    yield models_path

    if os.path.exists(models_path):
        os.rmdir(models_path)


@pytest.fixture
def create_example_repo(create_models_directory):
    repo_path = os.path.join(create_models_directory, 'example')
    os.mkdir(repo_path)

    yield 'example'

    os.rmdir(repo_path)


def test_list_repositories(create_example_repo):
    example_repo = create_example_repo

    result = runner.invoke(repository_app, ['list'])

    assert result.exit_code == 0
    assert example_repo in result.stdout.lower()


def test_use_repository(create_example_repo):
    _ = create_example_repo

    runner.invoke(repository_app, ['use', 'example'])

    assert get_config_file().get('repository_recovery_mode') == 'local'
    assert get_config_file().get('models_repository') == 'example'
