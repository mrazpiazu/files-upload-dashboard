from flask import Blueprint

public_bp = Blueprint('public', __name__, template_folder='public/templates/public', static_folder='static')

from . import routes