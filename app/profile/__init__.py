from flask import Blueprint

profile = Blueprint('profile', __name__, template_folder='../templates/templ-profile')

from . import views