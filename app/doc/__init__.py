from flask import Blueprint

doc = Blueprint('doc', __name__, static_folder='')

from . import views
