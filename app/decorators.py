from flask import current_app
from flask_login import current_user
from functools import wraps

def coach_required(func):
    
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.id_coach != None:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
    
