from flask import Blueprint

article = Blueprint('articulos', __name__, template_folder='templates')

from . import routes