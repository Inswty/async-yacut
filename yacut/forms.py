from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, MultipleFileField
from wtforms import URLField
from wtforms.validators import DataRequired, Length, Optional

from .constants import MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


class IndexForm(FlaskForm):
    original_link = URLField(
        'Добавьте оригинальную длинную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, MAX_ORIGINAL_LINK_LENGTH)]
    )
    custom_id = URLField(
        'Ваш вариант короткого идентификатора',
        validators=[Length(1, MAX_SHORT_LINK_LENGTH), Optional()]
    )


class UploadFileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[
            FileRequired(message="Файл обязателен для загрузки"),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                        message='Разрешены только файлы: jpg, jpeg, png, gif')
        ]
    )
