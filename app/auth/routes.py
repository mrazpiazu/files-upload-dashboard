from flask import flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import login_manager
from . import auth_bp
from .forms import RegistrationForm, LoginForm
from .models import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is None or user.check_password(form.password.data) is False:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login', form=form))

        login_user(user, remember=form.remember.data)
        return redirect(url_for('private.profile'))

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data

        user = User.get_by_email(email)

        if user is not None:
            flash('Email address already exists')
            return redirect(url_for('auth.signup', form=form))

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)

        if email == 'admin@mail.com':
            user.is_admin = True

        user.save()

        login_user(user, remember=True)

        return redirect(url_for('public.index'))

    return render_template('auth/signup_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))
