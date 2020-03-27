from flask import Blueprint

users = Blueprint('usuarios', __name__, template_folder='templates')

from . import routes