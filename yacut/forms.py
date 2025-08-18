from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


class LinkForm(FlaskForm):
    original_link = URLField(
        'Добавьте оригинальную длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, MAX_ORIGINAL_LINK_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант короткого идентификатора',
        validators=[
            Length(1, MAX_SHORT_LINK_LENGTH), Optional(),
            Regexp(r'^[a-zA-Z0-9]+$', message="Можно только латинские буквы и цифры")
        ]
    )


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            FileRequired(message="Файл обязателен для загрузки")
        ]
    )
