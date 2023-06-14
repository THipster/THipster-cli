import os
import json
import pytest
from pathlib import Path
from typer import get_app_dir
import thipstercli.constants as constants
from thipstercli.config import init_parameters


@pytest.fixture
def init_app_state():
    init_parameters()
    yield


@pytest.fixture
def config_path():
    return Path(get_app_dir(constants.APP_NAME)) / constants.CONFIG_FILE_NAME


@pytest.fixture
def create_config_file(config_path):
    if not os.path.exists(config_path):
        config_path.parent.mkdir(parents=True, exist_ok=True)

    yield config_path

    if os.path.exists(config_path):
        os.remove(config_path)


@pytest.fixture
def config_file(
    create_config_file,
):
    create_config_file.write_text("""{
        "app_name": "thipstercli",
        "auth_provider": "google",
        "input_dir": "test_input_directory",
        "local_models_repository_path": "models",
        "models_repository": "THipster/models",
        "models_repository_branch": "main",
        "models_repository_provider": "local",
        "output_dir": ".",
        "verbose": true
}""")

    init_parameters()

    yield


@pytest.fixture
def config_file_wrong_provider(create_config_file):
    create_config_file.write_text("""{"auth_provider": "notfound"}""")
    init_parameters()
    yield


@pytest.fixture
def get_config_file(config_path):
    yield json.loads(config_path.read_text())
