from flask import abort, jsonify, request
from http import HTTPStatus

from . import app
from .models import URLMap

MSG_ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    data = request.get_json(silent=True)
    URLMap.validate_for_api(data)
    urlmap = URLMap.create_new(data.get('url'), data.get('custom_id'))
    return jsonify({
        'url': urlmap.original,
        'short_link': request.host_url + urlmap.short
    }), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=('GET',))
def get_original_url(short):
    urlmap = URLMap.get_by_short(short)
    if not urlmap:
        abort(404, description=MSG_ID_NOT_FOUND)
    return jsonify({
        'url': urlmap.original,
    })
