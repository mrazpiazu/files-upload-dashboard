import os
from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required
from . import admin_bp
from ..auth.models import User
from ..private.models import File
from app.auth.decorators import admin_required


@admin_bp.route('/admin')
@login_required
@admin_required
def admin():
    users = User.get_all()
    return render_template('admin/admin.html', users=users)


@admin_bp.route('/user_config/<int:user_id>')
@login_required
@admin_required
def user_config(user_id):
    user = User.get_by_id(user_id)
    if user.is_admin:
        user.is_admin = False
    else:
        user.is_admin = True
    user.save()
    return redirect((url_for('admin.admin')))


@admin_bp.route('/delete_entry/<path:access>/<path:item>/<string:entry_id>')
@login_required
@admin_required
def delete_entry(access, item, entry_id):
    if item == 'user':
        entry = User.get_by_id(entry_id)
        url = 'admin.admin'
    elif item == 'file':
        entry = File.get_by_id(entry_id)
        if access == 'all_files':
            url = 'private.all_files'
        else:
            url = 'private.my_files'
        file_name = entry.file_name
        files_dir = current_app.config['FILES_DIR']
        os.makedirs(files_dir, exist_ok=True)
        file_path = os.path.join(files_dir, file_name)
        try:
            os.remove(file_path)
        except:
            flash('File does not exist.')

    if entry is None:
        abort(404)

    entry.delete()

    return redirect(url_for(url))