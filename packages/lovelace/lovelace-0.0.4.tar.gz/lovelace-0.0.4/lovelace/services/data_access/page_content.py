from typing import (Optional,
                    Tuple,
                    List)

from aiohttp import ClientSession

from lovelace.utils import join_str
from .wikipedia import query_wikipedia_api


async def fetch_pages_contents(*pages_ids: Tuple[str, ...],
                               session: ClientSession
                               ) -> List[Optional[str]]:
    params = dict(prop='extracts',
                  explaintext='',
                  rvprop='ids',
                  pageids=join_str(pages_ids,
                                   sep='|'))
    response = await query_wikipedia_api(**params,
                                         session=session)
    query = response['query']
    pages_info = query['pages']
    contents = []
    for page_id in pages_ids:
        page_info = pages_info[page_id]
        try:
            content = page_info['extract']
        except KeyError:
            content = None
        contents.append(content)
    return contents
