from http import HTTPStatus

from flask import jsonify, request

from . import app
from .models import URLMap

REQUEST_NO_BODY = 'Отсутствует тело запроса'
SHORT_NOT_FOUND = 'Указанный id не найден'
URL_REQUIRED = '"url" является обязательным полем!'


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise URLMap.InvalidAPIUsage(
            REQUEST_NO_BODY, status_code=HTTPStatus.BAD_REQUEST
        )
    try:
        url_map = URLMap.create(
            data['url'],
            data.get('custom_id'),
            is_api=True
        )
    except KeyError:
        raise URLMap.InvalidAPIUsage(
            URL_REQUIRED,
            status_code=HTTPStatus.BAD_REQUEST
        )
    return (
        jsonify({
            'url': url_map.original,
            'short_link': url_map.get_short_link(),
        }), HTTPStatus.CREATED
    )


@app.route('/api/id/<short>/', methods=('GET',))
def get_original_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise URLMap.InvalidAPIUsage(
            SHORT_NOT_FOUND, status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({
        'url': url_map.original,
    })
