from typing import Iterator

from lovelace.utils import lines_generator


def parse_page_sections_names(content: str
                              ) -> Iterator[str]:
    content_lines = lines_generator(content)
    sections_lines = filter(is_section_title, content_lines)
    for line in sections_lines:
        yield line.strip(' =')


def parse_page_section_content_lines(section_name: str,
                                     content: str
                                     ) -> Iterator[str]:
    section_title = f'== {section_name} =='
    content_lines = lines_generator(content)
    next(line for line in content_lines if line == section_title)
    for line in content_lines:
        line_is_section_title = is_section_title(line)
        if line_is_section_title:
            return
        yield line


def is_section_title(line: str) -> bool:
    section_line_head, section_line_tail = '== ', ' =='
    return (line.startswith(section_line_head) and
            line.endswith(section_line_tail))
