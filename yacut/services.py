import random
import string

from .constants import DEFAULT_SHORT_LINK_LENGTH


def get_unique_short_id():
    """Генерация случайного короткого идентификатора ссылки."""
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits, k=DEFAULT_SHORT_LINK_LENGTH
        )
    )
