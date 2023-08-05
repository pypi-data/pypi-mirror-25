import re
from typing import (Iterator,
                    Iterable)

LINE_RE = re.compile('^.+$', flags=re.MULTILINE)


def lines_generator(source: str) -> Iterator[str]:
    return (match.group(0)
            for match in LINE_RE.finditer(source))


def join_str(items: Iterable,
             *,
             sep: str = ', ') -> str:
    return sep.join(map(str, items))
