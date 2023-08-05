import pytest
from aiohttp import ClientSession

from lovelace.services.data_access import (fetch_pages_ids,
                                           fetch_titles)
from tests.strategies import (MIN_PAGE_ID,
                              MAX_PAGE_ID)

MAX_TITLE_LENGTH_IN_BYTES = 255


@pytest.mark.asyncio
async def test_fetch_titles(page_id: str,
                            invalid_page_id: str,
                            client_session: ClientSession) -> None:
    fetched_title, = await fetch_titles(page_id,
                                        session=client_session)
    assert (fetched_title is None or
            isinstance(fetched_title, str) and
            # https://en.wikipedia.org/wiki/Wikipedia:Page_name#Technical_restrictions_and_limitations
            len(fetched_title.encode()) <= MAX_TITLE_LENGTH_IN_BYTES and
            (fetched_title[0] == 'ß' or fetched_title[0].isupper()))

    with pytest.raises(IOError):
        await fetch_titles(invalid_page_id,
                           session=client_session)


@pytest.mark.asyncio
async def test_parse_page_id(title: str,
                             invalid_title: str,
                             client_session: ClientSession) -> None:
    none_page_id, = await fetch_pages_ids(invalid_title,
                                          session=client_session)
    page_id, = await fetch_pages_ids(title,
                                     session=client_session)

    assert none_page_id is None
    assert (page_id is None or
            MIN_PAGE_ID < int(page_id) < MAX_PAGE_ID)
