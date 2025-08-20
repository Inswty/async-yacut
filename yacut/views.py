from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import LinkForm, UploadFileForm
from .models import URLMap
from .yandex_disk import async_upload_files_to_yandex_disk

SHORT_NOT_FOUND = 'Указанный id не найден'


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data
        )
    except URLMap.WebAppError as e:
        flash(str(e), 'error')
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short_link=url_map.get_short_link()
    ), HTTPStatus.OK


@app.route('/<string:short>')
def redirect_view(short):
    url_map = URLMap.get(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND, description=SHORT_NOT_FOUND)
    return redirect(url_map.original)


@app.route('/files', methods=('GET', 'POST'))
async def upload_view():
    form = UploadFileForm()
    uploaded_files = []
    if not form.validate_on_submit():
        return render_template('upload.html', form=form, files=uploaded_files)
    # Асинхронная загрузка файлов
    urls = await async_upload_files_to_yandex_disk(form.files.data)
    # Собираем список загруженных файлов с подстраховкой на ошибки
    try:
        uploaded_files = [
            {
                'filename': file,
                'short': URLMap.create(url).short if url else None
            } for file, url in urls.items()
        ]
    except URLMap.InvalidAPIUsage as e:
        flash(str(e), 'error')
    return render_template('upload.html', form=form, files=uploaded_files)
