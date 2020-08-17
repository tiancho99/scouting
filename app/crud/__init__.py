from flask import Blueprint

crud = Blueprint('crud', __name__, template_folder='../templates/templ-crud')

from . import views