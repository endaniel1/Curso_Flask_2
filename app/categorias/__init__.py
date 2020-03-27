from flask import Blueprint

category = Blueprint('categorias', __name__, template_folder='templates')

from . import routes