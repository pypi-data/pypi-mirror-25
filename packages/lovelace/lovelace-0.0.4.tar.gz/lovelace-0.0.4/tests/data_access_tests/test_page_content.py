import re
import string

import pytest
from aiohttp import ClientSession

from lovelace.services.data_access import fetch_pages_contents


@pytest.mark.asyncio
async def test_fetch_page_content(page_id: str,
                                  client_session: ClientSession) -> None:
    page_content, = await fetch_pages_contents(page_id,
                                               session=client_session)

    if not page_content:
        return

    page_content_without_whitespaces = re.sub(pattern=r'\s',
                                              repl='',
                                              string=page_content)
    latin_alphanumeric_characters = string.ascii_letters + string.digits
    latin_alphanumeric_characters_count = sum(
        character in latin_alphanumeric_characters
        for character in page_content_without_whitespaces)
    latin_alphanumeric_characters_frequency = (
        latin_alphanumeric_characters_count
        / len(page_content_without_whitespaces))

    min_latin_alphanumeric_symbols_frequency = 0.5

    assert (latin_alphanumeric_characters_frequency == 0 or
            latin_alphanumeric_characters_frequency
            >= min_latin_alphanumeric_symbols_frequency)
