import random
from datetime import datetime

from . import db
from .error_handlers import InvalidAPIUsage, WebAppError
from .constants import (
    DEFAULT_SHORT_LENGTH, FORBIDDEN_SHORT_IDS, MAX_GENERATION_ATTEMPTS,
    MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH, SHORT_CHARS
)

from .constants import DEFAULT_SHORT_LENGTH


MSG_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
MSG_NO_BODY = 'Отсутствует тело запроса'
MSG_NO_URL = '\"url\" является обязательным полем!'
MSG_SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
MSG_SHOT_NOT_GEN = 'Не удалось сгенерировать уникальную короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def validate_for_web(cls, short: str | None):
        if short and not cls.validate_short(short):
            if short in FORBIDDEN_SHORT_IDS:
                raise WebAppError(MSG_SHORT_EXISTS)
            raise WebAppError(MSG_INVALID_SHORT)
        if short and cls.query.filter_by(short=short).first():
            raise WebAppError(MSG_SHORT_EXISTS)

    @classmethod
    def validate_for_api(cls, data):
        """Валидация для API."""
        if not data:
            raise InvalidAPIUsage(MSG_NO_BODY)
        if 'url' not in data:
            raise InvalidAPIUsage(MSG_NO_URL)
        short = data.get('custom_id')
        if short and not cls.validate_short(short):
            raise InvalidAPIUsage(MSG_INVALID_SHORT)
        if short and cls.query.filter_by(short=short).first():
            raise InvalidAPIUsage(MSG_SHORT_EXISTS)

    @classmethod
    def create_new(cls, url: str, short: str = None):
        if not short:
            short = cls.get_unique_short()
        urlmap = URLMap(original=url, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @classmethod
    def get_by_short(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def get_unique_short(cls):
        for _ in range(MAX_GENERATION_ATTEMPTS):
            short = ''.join(
                random.choices(
                    SHORT_CHARS, k=DEFAULT_SHORT_LENGTH
                )
            )
            if not cls.query.filter_by(short=short).first():
                return short
        raise RuntimeError(MSG_SHOT_NOT_GEN)

    @classmethod
    def validate_short(cls, short):
        return (
            isinstance(short, str)
            and len(short) <= MAX_SHORT_LENGTH
            and all(c in SHORT_CHARS for c in short)
            and short not in FORBIDDEN_SHORT_IDS
        )
