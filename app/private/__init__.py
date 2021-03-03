from flask import Blueprint

private_bp = Blueprint('private', __name__, template_folder='private/templates/admin')

from . import routes