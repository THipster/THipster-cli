"""Configuration module for the application."""
import json
from pathlib import Path

from rich import print
from typer import get_app_dir

import thipstercli.constants as constants
from thipstercli.helpers import check_thipster_module_exists

state = {}

app_dir = get_app_dir(constants.APP_NAME)
config_path: Path = Path(app_dir) / constants.CONFIG_FILE_NAME


def init_parameters() -> None:
    """Initialize the state of the application."""
    if not config_path.is_file():
        set_default_config()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(state, sort_keys=True, indent=4))
        return

    state.update(json.loads(config_path.read_text()))

    if not state.get('auth_provider'):
        return

    if not check_thipster_module_exists('auth', state['auth_provider']):
        print(f':rotating_light: User set Auth Provider [red]{state["auth_provider"]}\
[/red] not found')
        state.pop('auth_provider')


def set_default_config() -> None:
    """Set the default values for the user configuration file."""
    state['app_name'] = constants.APP_NAME
    state['verbose'] = constants.VERBOSE
    state['models_repository_provider'] = constants.MODELS_REPOSITORY_PROVIDER
    state['models_repository'] = constants.MODELS_REPOSITORY
    state['models_repository_branch'] = constants.MODELS_REPOSITORY_BRANCH
    state['local_models_repository_path'] = constants.LOCAL_MODELS_REPOSITORY_PATH
    state['input_dir'] = constants.INPUT_DIR
    state['output_dir'] = constants.OUTPUT_DIR


def update_config_file(parameters: dict[str, object]) -> None:
    """Update the config file with the given parameters."""
    if config_path.is_file():
        config_file: dict[str, object] = json.loads(config_path.read_text())
        config_file.update(parameters)
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_file = parameters

    config_path.write_text(json.dumps(config_file, sort_keys=True, indent=4))
