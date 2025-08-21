import random
from datetime import datetime

from flask import url_for

from settings import REDIRECT_LINK_ENDPOINT
from . import db
from .constants import (
    DEFAULT_SHORT_LENGTH, FORBIDDEN_SHORTS, MAX_GENERATION_ATTEMPTS,
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

    @staticmethod
    def create(url, short=None, validate_input=False):
        if not validate_input:
            if len(url) > MAX_ORIGINAL_LINK_LENGTH:
                raise ValueError(INVALID_URL)
        if short:
            if not validate_input:
                if (
                    len(short) > MAX_SHORT_LENGTH
                    or not SHORT_REGEX.fullmatch(short)
                ):
                    raise ValueError(INVALID_SHORT)
            if short in FORBIDDEN_SHORTS or URLMap.get(short) is not None:
                raise ValueError(SHORT_EXISTS)
        else:
            short = URLMap.get_unique_short()

        url_map = URLMap(original=url, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(
                    SHORT_CHARS, k=DEFAULT_SHORT_LENGTH
                )
            )
            if not URLMap.get(short) is not None:
                return short
        raise RuntimeError(SHORT_NOT_GEN)

    def get_short_link(self):
        return url_for(
            REDIRECT_LINK_ENDPOINT,
            short=self.short, _external=True
        )
