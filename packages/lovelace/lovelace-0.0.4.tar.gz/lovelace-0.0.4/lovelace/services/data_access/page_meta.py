from typing import (Optional,
                    Iterator,
                    Tuple)

from aiohttp import ClientSession

from lovelace.utils import join_str
from .utils import (wrap_query_errors,
                    get_page_id,
                    get_title)
from .wikipedia import query_wikipedia_api


async def fetch_pages_ids(*titles: Tuple[str, ...],
                          session: ClientSession
                          ) -> Iterator[Optional[str]]:
    params = dict(prop='info',
                  titles=join_str(titles,
                                  sep='|'))

    response = await query_wikipedia_api(**params,
                                         session=session)

    with wrap_query_errors(KeyError,
                           titles=titles):
        query = response['query']
        pages_info = query['pages']

    with wrap_query_errors(AttributeError,
                           titles=titles):
        return map(get_page_id, pages_info.values())


async def fetch_titles(*pages_ids: Tuple[str, ...],
                       session: ClientSession
                       ) -> Iterator[Optional[str]]:
    params = dict(prop='info',
                  pageids=join_str(pages_ids,
                                   sep='|'))

    response = await query_wikipedia_api(**params,
                                         session=session)

    with wrap_query_errors(KeyError,
                           pages_ids=pages_ids):
        query = response['query']
        pages_info = query['pages']

    with wrap_query_errors(AttributeError,
                           pages_ids=pages_ids):
        return map(get_title, pages_info.values())
