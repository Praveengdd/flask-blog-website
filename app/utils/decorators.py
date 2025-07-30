from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
                
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in roles):
                abort(403)
                
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator