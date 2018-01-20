from flask import Blueprint

assessment = Blueprint('assessment', __name__, template_folder='templates')

from . import views
