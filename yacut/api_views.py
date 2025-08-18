from flask import abort, jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .services import get_unique_short_id
from .validators import validate_short_link


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    short_link = data.get('custom_id')
    if short_link and not validate_short_link(short_link):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url = data.get('url')
    if not url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if short_link and URLMap.query.filter_by(short=short_link).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if not short_link:
        short_link = get_unique_short_id()
        while URLMap.query.filter_by(short=short_link).first():
            short_link = get_unique_short_id()
    urlmap = URLMap(
        original=url,
        short=short_link
    )
    db.session.add(urlmap)
    db.session.commit()
    return jsonify({
        'url': url,
        'short_link': request.host_url + short_link
    }), 201


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_original_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        abort(404, description='Указанный id не найден')
    return jsonify({
        'url': urlmap.original,
    })