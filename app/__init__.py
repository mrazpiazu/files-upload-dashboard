from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import platform

login_manager = LoginManager()
db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    if platform.system() == "Windows":
        app.config['FILES_DIR'] = 'C:/SGDF'
    elif platform.system() == 'Linux':
        app.config['FILES_DIR'] = '/opt/SGDF'

    # Normalmente utilizaría app.config['MAX_CONTENT_LENGTH'] para establecer el tamaño máximo del body para la subida de ficheros y un errorhandler 413 para los ficheros que lo superen
    # El problema es que el "servidor" de desarrollo de Flask genera connection reset en lugar de gestionar el 413, así que lo dejo comentado y aplico una solución más "chapucera" en auth/routes.py (/upload_file)
    #app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['UPLOAD_EXTENSIONS'] = ['.jpeg', '.jpg', '.png', '.txt', '.doc', '.csv', '.pdf']
    app.config['SECRET_KEY'] = '554H65hNHGfhggh45H23R1h56H'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .public import public_bp
    app.register_blueprint(public_bp)
    from .private import private_bp
    app.register_blueprint(private_bp)

    register_error_handlers(app)

    return app


def register_error_handlers(app):

    @app.errorhandler(401)
    def error_401_handler(e):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(413)
    def error_413_handler(e):
        return render_template('413.html'), 413

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500
