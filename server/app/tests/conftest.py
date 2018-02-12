import pytest
from ..settings import DB_URI_TEST, DB_TEST_ON, DB_DEBUG_ON
from extensions.db import db
from .. import app
from .. import remote_script


key = "140b41b22a29beb4061bda66b6747e14"

@pytest.fixture(scope='session')
def test_app():
    return app.create_app('app/tests/test_config.xml')


@pytest.fixture(scope='session')
def test_aes_cipher():
    return remote_script.AESCipher(key)


@pytest.fixture(scope='session')
def test_stats_collector():
    return remote_script.StatisticsCollector()
