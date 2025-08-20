
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LENGTH,
                        SHORT_REGEX)

FIELD_REQUIRED = 'Обязательное поле'
FILE_REQUIRED = 'Файл обязателен для загрузки'
LABEL_ORIGINAL_LINK = 'Добавьте оригинальную длинную ссылку'
LABEL_SELECT_FILES = 'Выберите файлы'
LABEL_SHORT = 'Ваш вариант короткого идентификатора'
SHORT_INVALID = 'Можно только латинские буквы и цифры'


class LinkForm(FlaskForm):
    original_link = URLField(
        LABEL_ORIGINAL_LINK,
        validators=[
            DataRequired(message=FIELD_REQUIRED),
            Length(max=MAX_ORIGINAL_LINK_LENGTH)
        ]
    )
    custom_id = StringField(
        LABEL_SHORT,
        validators=[
            Optional(),
            Length(max=MAX_SHORT_LENGTH),
            Regexp(SHORT_REGEX, message=SHORT_INVALID)
        ]
    )


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        LABEL_SELECT_FILES,
        validators=[
            FileRequired(message=FILE_REQUIRED)
        ]
    )
