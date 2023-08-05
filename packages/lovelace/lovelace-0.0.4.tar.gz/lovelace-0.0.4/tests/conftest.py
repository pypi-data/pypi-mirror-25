import os
import pkgutil
import sys
from asyncio import AbstractEventLoop, get_event_loop
from contextlib import closing
from typing import Generator

import pytest
from _pytest.config import Parser
from _pytest.python import Metafunc
from aiohttp import ClientSession

from lovelace.services.data_access.wikipedia import query_wikipedia_api

base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)

fixtures_pkg_name = 'fixtures'
fixtures_pkg_path = os.path.join(base_dir, fixtures_pkg_name)
pytest_plugins = [f'{fixtures_pkg_name}.{name}'
                  for _, name, _ in pkgutil.iter_modules([fixtures_pkg_path])]


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--repeat', action='store',
                     help='Number of times to repeat each test')


def pytest_generate_tests(metafunc: Metafunc) -> None:
    if metafunc.config.option.repeat is not None:
        count = int(metafunc.config.option.repeat)
        # We're going to duplicate these tests by parametrizing them,
        # which requires that each test has a fixture to accept the parameter.
        # We can add a new fixture like so:
        metafunc.fixturenames.append('tmp_ct')
        # Now we parametrize. This is what happens when we do e.g.,
        # @pytest.mark.parametrize('tmp_ct', range(count))
        # def test_foo(): pass
        metafunc.parametrize('tmp_ct', range(count))


@pytest.fixture(scope='function')
def client_session(event_loop: AbstractEventLoop
                   ) -> Generator[ClientSession, None, None]:
    res = ClientSession(loop=event_loop)
    with closing(res):
        yield res


@pytest.fixture(scope='session',
                autouse=True)
def preparation() -> None:
    loop = get_event_loop()
    session = ClientSession(loop=loop)
    with closing(session):
        loop.run_until_complete(query_wikipedia_api(session=session))
