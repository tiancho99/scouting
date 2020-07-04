from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


from .config import Config
from .models import Athlete

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return Athlete.query.get(user_id)
    return None

def create_app():
    # create flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    #initialize plugins
    from .models import db
    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # bring blueprints
    from .auth import auth
    from .profile import profile

    # register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(profile, url_prefix='/profile')
    return app
