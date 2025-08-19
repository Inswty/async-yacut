from flask import flash, jsonify, render_template, request
from http import HTTPStatus

from . import app, db
from .forms import LinkForm

MSG_ID_NOT_FOUND = 'Указанный id не найден'


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    if request.path.startswith('/api/'):
        return (
            jsonify({'message': MSG_ID_NOT_FOUND}),
            HTTPStatus.NOT_FOUND
        )
    # Для обычных страниц возвращаем HTML
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


class WebAppError(Exception):
    """Общее исключение для ошибок пользовательского интерфейса."""
    pass


@app.errorhandler(WebAppError)
def handle_web_error(e):
    flash(str(e), 'error')
    return (
        render_template('index.html', form=LinkForm()), HTTPStatus.BAD_REQUEST
    )
