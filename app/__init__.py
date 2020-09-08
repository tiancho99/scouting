from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_wtf import CsrfProtect

from .config import Config
from .models import Person

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Person.query.get(user_id)
    return None

def create_app():
    # create flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    #initialize plugins
    from .models import db, ma
    Bootstrap(app)
    db.init_app(app)
    ma.init_app(app)
    db.create_all()
   
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # csrf = CsrfProtect(app)

    # bring blueprints
    from .auth import auth
    from .profile import profile
    from .crud import crud

    # register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(crud, url_prefix='/crud')
    return app
