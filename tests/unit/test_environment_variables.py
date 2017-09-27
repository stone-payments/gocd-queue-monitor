import os
import pytest
from src.app.utils.EnvironmentVariables import EnvironmentVariables
from dotenv import load_dotenv

@pytest.fixture
def load_envs():
    print('Loading envs')
    envs_loaded = load_dotenv(os.path.dirname(__file__) + '/../files/' + '.envtest')
    yield envs_loaded
    print('Unloading envs')
    del(os.environ["GOCD_API_URL"])
    del(os.environ["GOCD_USER"])
    del(os.environ["GOCD_PASSWORD"])
    del(os.environ["PORT"])

@pytest.fixture
def environment_variables():
    return EnvironmentVariables()

def test_should_import_env_file_and_load_env_vars(load_envs):

    assert load_envs is True


def test_gocd_api_url_env_var_must_be_set(load_envs):

    assert os.environ.get("GOCD_API_URL") == 'https://cd.teste.com.br:1234/go/api'


def test_gocd_api_url_env_var_must_be_the_endpoint_api(load_envs):

    assert os.environ.get("GOCD_API_URL").endswith('/api')


def test_gocd_user_env_var_must_be_set(load_envs):

    assert os.environ.get("GOCD_USER") == 'testeuser'


def test_gocd_password_env_var_must_be_set(load_envs):

    assert os.environ.get("GOCD_PASSWORD") == 'testpass'


def test_port_env_var_must_be_set(load_envs):

    assert os.environ.get("PORT") == '8888'


def test_port_should_be_able_to_convert_to_int(load_envs):
    port_int = int(os.environ.get("PORT"))
    assert port_int == 8888


def test_environment_variables_gocd_api_url(load_envs,environment_variables):

    assert environment_variables.gocd_api_url() ==  'https://cd.teste.com.br:1234/go/api'


def test_environment_variables_gocd_user(load_envs,environment_variables):

    assert environment_variables.gocd_user() ==  'testeuser'


def test_environment_variables_gocd_password(load_envs,environment_variables):

    assert environment_variables.gocd_password() ==  'testpass'


def test_environment_variables_port(load_envs,environment_variables):

    assert environment_variables.port() ==  8888