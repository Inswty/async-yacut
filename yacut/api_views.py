from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

REQUEST_NO_BODY = 'Отсутствует тело запроса'
SHORT_NOT_FOUND = 'Указанный id не найден'
URL_REQUIRED = '"url" является обязательным полем!'


@app.route('/api/id/', methods=('POST',))
def add_url_mapping():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage(
            REQUEST_NO_BODY
        )
    if 'url' not in data:
        raise InvalidAPIUsage(
            URL_REQUIRED
        )
    try:
        return (
            jsonify({
                'url': data['url'],
                'short_link': URLMap.create(
                    data['url'],
                    data.get('custom_id'),
                ).get_short_link(),
            }),
            HTTPStatus.CREATED
        )
    except (ValueError, RuntimeError) as e:
        raise InvalidAPIUsage(str(e))


@app.route('/api/id/<short>/', methods=('GET',))
def get_original_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsage(
            SHORT_NOT_FOUND, status_code=HTTPStatus.NOT_FOUND
        )
    return jsonify({
        'url': url_map.original,
    })
