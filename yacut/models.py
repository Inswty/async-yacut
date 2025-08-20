import random
from http import HTTPStatus
from datetime import datetime
from urllib.parse import urlparse

from flask import url_for

from settings import REDIRECT_LINK_ENDPOINT
from . import db
from .constants import (
    DEFAULT_SHORT_LENGTH, FORBIDDEN_SHORT, MAX_GENERATION_ATTEMPTS,
    MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH, SHORT_CHARS, SHORT_REGEX
)

INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
INVALID_URL = 'Некорректный URL'
NO_BODY = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
SHORT_NOT_GEN = 'Не удалось сгенерировать уникальную короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    class WebAppError(Exception):
        """Общее исключение для ошибок пользовательского интерфейса."""

        pass

    class InvalidAPIUsage(Exception):
        """Общее исключение для ошибок API."""

        status_code = HTTPStatus.BAD_REQUEST

        def __init__(self, message, status_code=None):
            super().__init__()
            self.message = message
            if status_code is not None:
                self.status_code = status_code

        def to_dict(self):
            return dict(message=self.message)

    @staticmethod
    def is_valid_url(url):
        """Проверяет, что URL корректный, содержит http/https и домен."""
        try:
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except Exception:
            return False

    @classmethod
    def create(cls, url, short=None, is_api=False):
        if not cls.is_valid_url(url):
            if is_api:
                raise cls.InvalidAPIUsage(
                    INVALID_URL,
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                raise cls.WebAppError(INVALID_URL)
        if short and not (
            SHORT_REGEX.fullmatch(short) is not None
            and len(short) <= MAX_SHORT_LENGTH
        ):
            if is_api:
                raise cls.InvalidAPIUsage(
                    INVALID_SHORT,
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                raise cls.WebAppError(INVALID_SHORT)
        if short in FORBIDDEN_SHORT:
            if is_api:
                raise cls.InvalidAPIUsage(
                    SHORT_EXISTS,
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                raise cls.WebAppError(SHORT_EXISTS)
        if short and cls.get(short) is not None:
            if is_api:
                raise cls.InvalidAPIUsage(
                    SHORT_EXISTS,
                    status_code=HTTPStatus.BAD_REQUEST
                )
            else:
                raise cls.WebAppError(SHORT_EXISTS)
        if not short:
            short = cls.get_unique_short()
        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @classmethod
    def get(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def get_unique_short(cls):
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(
                    SHORT_CHARS, k=DEFAULT_SHORT_LENGTH
                )
            )
            if not cls.get(short) is not None:
                return short
        raise RuntimeError(SHORT_NOT_GEN)

    def get_short_link(self):
        return url_for(
            REDIRECT_LINK_ENDPOINT,
            short=self.short, _external=True
        )
