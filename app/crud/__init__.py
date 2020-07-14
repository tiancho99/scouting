from flask import Blueprint

crud = Blueprint('crud', __name__, template_folder='../templates/templ_crud')

from . import views