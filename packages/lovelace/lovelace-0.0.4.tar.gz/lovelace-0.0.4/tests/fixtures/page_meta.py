from asyncio import AbstractEventLoop

import pytest
from aiohttp import ClientSession

from lovelace.services.data_access import fetch_titles
from tests.strategies import (pages_ids_strategy,
                              non_digit_strings_strategy)
from tests.strategies.page_meta import invalid_pages_titles_strategy


@pytest.fixture(scope='function')
def page_id() -> str:
    return str(pages_ids_strategy.example())


@pytest.fixture(scope='function')
def invalid_page_id() -> str:
    return non_digit_strings_strategy.example()


@pytest.fixture(scope='function')
def title(page_id: str,
          client_session: ClientSession,
          event_loop: AbstractEventLoop) -> str:
    resp = event_loop.run_until_complete(fetch_titles(page_id,
                                                      session=client_session))
    res, = resp
    # "None" is a valid page title
    return str(res)


@pytest.fixture(scope='function')
def invalid_title() -> str:
    return invalid_pages_titles_strategy.example()
