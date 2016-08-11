from flask import Blueprint

manage = Blueprint('manage', __name__, static_folder='')

from . import views
