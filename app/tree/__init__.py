from flask import Blueprint

tree = Blueprint('tree', __name__, static_folder='')

from . import views
