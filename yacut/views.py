from flask import abort, redirect, render_template, url_for
from http import HTTPStatus

from . import app
from .forms import LinkForm, UploadFileForm
from .models import URLMap
from .yandex_disk import async_upload_files_to_yandex_disk

MSG_ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = LinkForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    URLMap.validate_for_web(form.custom_id.data)
    urlmap = URLMap.create_new(
        url=form.original_link.data,
        short=form.custom_id.data
    )
    return render_template(
        'index.html', form=form,
        short_link=url_for('follow_link', short=urlmap.short, _external=True)
    )


@app.route('/<string:short>')
def follow_link(short):
    urlmap = URLMap.get_by_short(short)
    if not urlmap:
        abort(HTTPStatus.NOT_FOUND, description=MSG_ID_NOT_FOUND)
    return redirect(urlmap.original)


@app.route('/files', methods=('GET', 'POST'))
async def upload_view():
    form = UploadFileForm()
    uploaded_files = []
    if not form.validate_on_submit():
        return render_template('upload.html', form=form, files=uploaded_files)
    urls = await async_upload_files_to_yandex_disk(form.files.data)
    for file, url in urls.items():
        urlmap = URLMap.create_new(url)
        uploaded_files.append({
            'filename': file,
            'short': urlmap.short
        })
    return render_template('upload.html', form=form, files=uploaded_files)
