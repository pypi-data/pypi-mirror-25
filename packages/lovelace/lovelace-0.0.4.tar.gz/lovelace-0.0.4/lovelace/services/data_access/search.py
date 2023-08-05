from typing import (Any,
                    Dict,
                    List)

from aiohttp import ClientSession

from .utils import wrap_query_errors
from .wikipedia import query_wikipedia_api


async def search_page_title(title_part: str,
                            *,
                            session: ClientSession,
                            results_count: int = 10
                            ) -> List[str]:
    params = dict(list='search',
                  srprop='',
                  srlimit=results_count,
                  limit=results_count,
                  srsearch=title_part)

    response = await query_wikipedia_api(**params,
                                         session=session)
    validate_response(response)

    with wrap_query_errors(KeyError,
                           title_part=title_part):
        query = response['query']
        results = query['search']

    return [result['title'] for result in results]


def validate_response(response: Dict[str, Any]
                      ) -> None:
    errors_messages = response.get('error')
    if errors_messages is None:
        return
    errors_messages_info = errors_messages['info']
    raise IOError(errors_messages_info)
