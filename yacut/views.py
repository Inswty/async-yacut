from flask import abort, flash, redirect, render_template


from . import app, db
from .forms import LinkForm, UploadFileForm
from .models import URLMap
from .services import get_unique_short_id
from .yandex_disk import async_upload_files_to_yandex_disk


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        if form.custom_id.data:
            short_link = form.custom_id.data
            if (
                URLMap.query.filter_by(short=short_link).first() or
                short_link == 'files'
            ):
                flash('Предложенный вариант короткой ссылки уже существует.',
                      'error')
                return render_template('main.html', form=form)
        else:
            while True:
                short_link = get_unique_short_id()
                if not URLMap.query.filter_by(short=short_link).first():
                    break
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('main.html', form=form, short_link=short_link)
    return render_template('main.html', form=form)


@app.route('/<string:short>')
def follow_link(short):
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)


@app.route('/files', methods=('GET', 'POST'))
async def upload_view():
    form = UploadFileForm()
    uploaded_files = []
    if form.validate_on_submit():
        urls = await async_upload_files_to_yandex_disk(form.files.data)
        for file, url in urls.items():
            # генерируем уникальный short
            while True:
                short_link = get_unique_short_id()
                if not URLMap.query.filter_by(short=short_link).first():
                    break
            urlmap = URLMap(
                original=url,
                short=short_link
            )
            db.session.add(urlmap)
            uploaded_files.append({
                'filename': file,
                'short': short_link
            })
        db.session.commit()
    return render_template('upload.html', form=form, files=uploaded_files)
