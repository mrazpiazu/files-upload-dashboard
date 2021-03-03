import os
from flask import current_app, render_template, redirect, url_for, send_from_directory, flash, abort
from flask_login import login_required, current_user
from .forms import FileForm
from .models import File
from . import private_bp
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import hashlib


def pretty_files(files):
    for file in files:
        file.created = file.created.strftime("%Y-%m-%d %H:%M:%S")
        if round(int(file.size) / 1024, 2) >= 1:
            file.size = str(round(int(file.size) / 1024 / 1024, 2)) + ' Mb'
        else:
            file.size = str(round(int(file.size) / 1024, 2)) + ' Kb'
    return files


@private_bp.route('/my_files')
@login_required
def my_files():
    files = pretty_files(File.get_by_user(current_user.id))
    return render_template('private/my_files.html', name=current_user.first_name, files=files)


@private_bp.route('/all_files')
@login_required
def all_files():
    files = pretty_files(File.get_all())
    return render_template('private/all_files.html', name=current_user.first_name, files=files)


@private_bp.route('/download_file/<path:file_hash>')
@login_required
def download_file(file_hash):
    file_name = File.get_by_hash(file_hash).file_name
    return send_from_directory(directory=current_app.config['FILES_DIR'], filename=file_name, as_attachment=True)


@private_bp.route('/profile')
@login_required
def profile():
    return render_template('private/profile.html', name=current_user.first_name)


@private_bp.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_file():
    #try:
    #    form = FileForm()
    #except RequestEntityTooLarge as e:
    #    abort(413)
    form = FileForm()
    if form.validate_on_submit():
        if os.path.splitext(form.file.data.filename)[1] not in current_app.config['UPLOAD_EXTENSIONS']:
            abort(413)
        file = form.file.data
        if file:
            title = form.title.data
            description = form.description.data
            file_name = secure_filename(file.filename)
            files_dir = current_app.config['FILES_DIR']
            blob = file.read()
            # Solución "chapucera" que comentaba en __init__.py #
            if len(blob) > 16 * 1024 * 1024:
                flash('File too large (max. 16Mb')
                return render_template('private/upload-file.html', form=form)
            ####################################################
            hash_key = hashlib.sha256(blob).hexdigest()
            if File.get_by_hash(hash_key) is not None:
                flash('This file already exists in the server.')
                return render_template('private/upload-file.html', form=form)
            file.seek(0)
            os.makedirs(files_dir, exist_ok=True)
            file_path = os.path.join(files_dir, file_name)
            file.save(file_path)

            file = File(
                user_id=current_user.id,
                user_email=current_user.email,
                title=title,
                file_name=file_name,
                description=description,
                size=len(blob),
                hash=hash_key)

            file.save()

            return redirect(url_for('private.my_files'))

    return render_template('private/upload-file.html', form=form)

