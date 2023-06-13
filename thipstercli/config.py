import json
from pathlib import Path
from typer import get_app_dir
import thipstercli.constants as constants

state = {}

app_dir = get_app_dir(constants.APP_NAME)
config_path: Path = Path(app_dir) / constants.CONFIG_FILE_NAME


def init_parameters() -> None:
    """Initializes the state
    """
    if not config_path.is_file():
        set_default_config()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(state))
        return

    state.update(json.loads(config_path.read_text()))


def set_default_config() -> None:
    """Sets the default configuration
    """
    state['app_name'] = constants.APP_NAME
    state['verbose'] = constants.VERBOSE
    state['github_repo'] = constants.GITHUB_REPO
    state['github_repo_branch'] = constants.GITHUB_REPO_BRANCH
    state['local_repo_path'] = constants.LOCAL_REPO_PATH
    state['providers'] = constants.PROVIDERS
    state['input_dir'] = constants.INPUT_DIR
    state['output_dir'] = constants.OUTPUT_DIR


def update_config_file(parameters: dict[str, object]) -> None:
    """Updates the config file
    """
    config_file: dict[str, object] = json.loads(config_path.read_text())
    config_file.update(parameters)
    config_path.write_text(json.dumps(config_file))