from flask import Blueprint

auth = Blueprint('auth', __name__, static_folder='')

from . import views
