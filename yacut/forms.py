import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH,
                        SHORT_CHARS)

LABEL_CUSTOM_ID = 'Ваш вариант короткого идентификатора'
LABEL_ORIGINAL_LINK = 'Добавьте оригинальную длинную ссылку'
MSG_FILE_REQUIRED = 'Файл обязателен для загрузки'
MSG_REQUIRED = 'Обязательное поле'
MSG_SHORT_INVALID = 'Можно только латинские буквы и цифры'


class LinkForm(FlaskForm):
    original_link = URLField(
        LABEL_ORIGINAL_LINK,
        validators=[
            DataRequired(message=MSG_REQUIRED),
            Length(max=MAX_ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        LABEL_CUSTOM_ID,
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LENGTH),
            Regexp(re.compile(f'^[{re.escape(SHORT_CHARS)}]+$'),
                   message=MSG_SHORT_INVALID)
        ]
    )


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            FileRequired(message=MSG_FILE_REQUIRED)
        ]
    )
