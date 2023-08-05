import string

from hypothesis import strategies

MIN_PAGE_ID = 1_000
MAX_PAGE_ID = 10_000_000
pages_ids_strategy = strategies.integers(min_value=MIN_PAGE_ID,
                                         max_value=MAX_PAGE_ID)

non_digit_strings_strategy = strategies.text(
    alphabet=strategies.characters(blacklist_characters=string.digits))

invalid_pages_titles_strategy = strategies.text(
    alphabet=strategies.characters(whitelist_categories=('Ll',)),
    min_size=5)
