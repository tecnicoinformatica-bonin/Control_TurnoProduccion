from functools import wraps
from flask import abort
from flask_login import current_user

def permiso_requerido(*permisos, require_all=False):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):

            if require_all:
                autorizado = all(
                    current_user.tiene_permiso(p)
                    for p in permisos
                )
            else:
                autorizado = any(
                    current_user.tiene_permiso(p)
                    for p in permisos
                )

            if not autorizado:
                abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator