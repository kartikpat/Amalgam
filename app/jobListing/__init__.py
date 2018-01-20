from flask import Blueprint

jobListing = Blueprint('jobListing', __name__, template_folder='templates')

from . import views
