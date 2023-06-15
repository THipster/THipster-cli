import os
import json
import shutil

from typing import Annotated
from git import Repo
import typer
from rich.panel import Panel
from rich import print
from .config import app_dir, state, update_config_file
from .display import error, warn

from .constants import LOCAL_MODELS_REPOSITORY_PATH

repository_app = typer.Typer(no_args_is_help=True)


@repository_app.callback()
def main():
    """Manage locally installed THipster repositories
    """


@repository_app.command('list')
def list():
    """List all the locally installed THipster repositories
    """
    downloaded_repos = list_installed_repos()

    repos_display = ''
    for repo in downloaded_repos:
        repos_display += f'[green]{repo}[/green]\n'
    print(Panel(repos_display, title='Locally installed model repositories'))
    __more_info_repos()


@repository_app.command('use')
def use(
    repository: Annotated[str, typer.Argument(help='The local repository to use')],
):
    """Set the repository to use


    """
    downloaded_repos = list_installed_repos()

    if repository not in downloaded_repos:
        state['repository_recovery_mode'] = 'online'
        warn('Model repository not locally installed, using online mode')
    else:
        state['repository_recovery_mode'] = 'local'

    state['models_repository'] = repository
    update_config_file(state)


@repository_app.command('download')
def download(
    url: Annotated[
        str,
        typer.Argument(
            help='The thipster repository to download. (*.git link)',
        ),
    ],
):
    """Download an online git repository as THipster repository
    """
    if not url.endswith('.git'):
        error('Use .git link to repository')

    repositories_path = os.path.join(app_dir, LOCAL_MODELS_REPOSITORY_PATH)
    if not os.path.exists(repositories_path):
        os.mkdir(repositories_path)

    clone_to = os.path.join('/tmp', 'thipster')
    Repo.clone_from(url, clone_to)

    with open(os.path.join(clone_to, 'thipster-config.json')) as f:
        config_path = f.read()

    try:
        config_file: dict = json.loads(config_path)
    except Exception as e:
        shutil.rmtree(clone_to)
        raise e

    repo_name = config_file.get('name')
    repo_directory = config_file.get('model_folder')

    if not (repo_name and repo_directory):
        shutil.rmtree(clone_to)
        error('Configuration error in thipster-config.json')

    if os.path.exists(repo_name):
        shutil.rmtree(clone_to)
        error(f'Repository named {repo_name} already installed')

    try:
        shutil.move(
            os.path.join(clone_to, repo_directory),
            os.path.join(repositories_path, repo_name),
        )
    except Exception:
        shutil.rmtree(clone_to)
        error('Configuration error in thipster-config.json : bad model_folder')

    shutil.rmtree(clone_to)


def list_installed_repos():
    downloaded_repos = []
    repositories_path = os.path.join(app_dir, LOCAL_MODELS_REPOSITORY_PATH)
    if os.path.exists(repositories_path):
        downloaded_repos = os.listdir(repositories_path)

    return downloaded_repos


def __more_info_repos():
    print(
        Panel('For more information about a provider, run: thipster repository info \
<repository>'),
    ) if state.get('verbose') else None
