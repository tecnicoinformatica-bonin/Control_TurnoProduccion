from functools import wraps
from flask_login import current_user
from flask import jsonify

def roles_required(*roles):

    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if not current_user.is_authenticated:
                return jsonify({"error": "No autenticado"}), 401

            if current_user.rol not in roles:
                return jsonify({"error": "Acceso denegado"}), 403

            return view(*args, **kwargs)

        return wrapped_view

    return decorator