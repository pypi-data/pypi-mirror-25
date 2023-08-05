from __future__ import absolute_import, print_function, unicode_literals

import os

import pytest


@pytest.fixture
def config():
    from zenaton.config import Config

    return Config()


@pytest.mark.parametrize('env_var,attr_name', [
    ('ZENATON_APP_ID', 'app_id'),
    ('ZENATON_APP_ENV', 'app_env'),
    ('ZENATON_API_TOKEN', 'api_token'),
])
def test_required_environment_variable(config, env_var, attr_name, monkeypatch):

    monkeypatch.delenv(env_var, raising=False)
    with pytest.raises(KeyError):
        getattr(config, attr_name)


def test_absolute_path_to_worker_script(config):
    assert os.path.isabs(config.worker_script)
