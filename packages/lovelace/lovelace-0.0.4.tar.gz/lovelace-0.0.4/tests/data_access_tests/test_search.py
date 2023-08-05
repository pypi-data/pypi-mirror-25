import pytest
from aiohttp import ClientSession

from lovelace.services.data_access import search_page_title


@pytest.mark.asyncio
async def test_search_page_title(title: str,
                                 client_session: ClientSession) -> None:
    search_results = await search_page_title(title_part=title,
                                             session=client_session)
    assert search_results
