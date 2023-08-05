from contextlib import contextmanager
from typing import (Any,
                    Optional,
                    Dict,
                    Tuple)

from lovelace.utils import join_str


@contextmanager
def wrap_query_errors(
        *errors: Tuple[Exception, ...],
        **kwargs: Dict[str, Any]):
    try:
        yield
    except errors as err:
        kwargs = {key: join_str(f'"{value}"' for value in values)
                  for key, values in kwargs.items()}
        kwargs_str = join_str(f'{key} {values_str}'
                              for key, values_str in kwargs.items())
        err_msg = (f'Error while querying pages '
                   f'with {kwargs_str}.')
        raise IOError(err_msg) from err


def get_page_id(page_info: Dict[str, Any]
                ) -> Optional[str]:
    try:
        return page_info['pageid']
    except KeyError:
        return None


def get_title(page_info: Dict[str, Any]
              ) -> Optional[str]:
    try:
        return page_info['title']
    except KeyError:
        return None
