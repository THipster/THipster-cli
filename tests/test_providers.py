"""Test the providers.py module."""
from typer.testing import CliRunner

from thipstercli.config import state
from thipstercli.helpers import get_auth_provider_class
from thipstercli.providers import app, check_provider_exists

from .conftest import get_config_file

runner = CliRunner(mix_stderr=False)

providers = [
    'google',
]


def test_list_providers():
    """Test the list command."""
    result = runner.invoke(app, ['list'])
    assert result.exit_code == 0
    for provider in providers:
        assert provider in result.stdout.lower()


def test_info_provider():
    """Test the info command for 'google'."""
    result = runner.invoke(app, ['info', 'google'])
    assert result.exit_code == 0
    assert 'google' in result.stdout.lower()
    assert 'gcloud' in result.stdout.lower()


def test_info_provider_not_found():
    """Test the info command for wrong provider 'notfound'."""
    result = runner.invoke(app, ['info', 'notfound'])
    assert result.exit_code == 1
    assert 'provider notfound not found.' in result.stdout.lower()


def test_set_provider():
    """Test the set command for 'google'."""
    result = runner.invoke(app, ['set', 'google'])
    assert result.exit_code == 0
    assert 'google' in result.stdout.lower()
    assert 'provider set to' in result.stdout.lower()


def test_set_provider_not_found():
    """Test the set command for wrong provider 'notfound'."""
    result = runner.invoke(app, ['set', 'notfound'])
    assert result.exit_code == 1
    assert 'provider notfound not found.' in result.stdout.lower()


def test_display_provider(config_file):
    """Test the display command for the 'google' provider set in the config file."""
    _ = config_file
    result = runner.invoke(app, ['display'])
    assert result.exit_code == 0
    assert 'provider set to' in result.stdout.lower()
    assert 'google' in result.stdout.lower()


def test_get_provider_class():
    """Test the get_auth_provider_class function."""
    provider = get_auth_provider_class('Google')
    assert provider.__name__ == 'GoogleAuth'


def test_check_provider_exists():
    """Test the check_provider_exists function."""
    provider = check_provider_exists('google')
    assert provider == 'google'


def test_set_provider_config_file(config_file_wrong_provider):
    """Test if the set command sets the provider in the config file."""
    _ = config_file_wrong_provider
    runner.invoke(app, ['set', 'google'])
    assert get_config_file().get('auth_provider', None) == 'google'


def test_wrong_provider_config_file(config_file_wrong_provider):
    """Test the behavior of the app when the config file has a wrong provider."""
    _ = config_file_wrong_provider
    runner.invoke(app, ['--help'])
    assert state.get('auth_provider', None) is None
