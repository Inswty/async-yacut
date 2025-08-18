import re

from .constants import MAX_SHORT_LINK_LENGTH, SHORT_LINK_REGEX


def validate_short_link(short_link):
    return (
        short_link is not None and
        1 <= len(short_link) <= MAX_SHORT_LINK_LENGTH and
        re.fullmatch(SHORT_LINK_REGEX, short_link) is not None
    )
