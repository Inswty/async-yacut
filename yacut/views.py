from flask import abort, flash, redirect, render_template, url_for


from . import app, db
from .forms import UploadFileForm


@app.route('/')
def index_view():
    return render_template('main.html')


@app.route('/files')
def upload_view():
    form = UploadFileForm()
    return render_template('upload.html', form=form)


def revers():
    pass
