
from functools import wraps
from flask import request, session, redirect, url_for, flash
from flask_login import current_user
from app.extensions.messages import FlashMessages

def ruta_requerida():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:
                return redirect(url_for("usuario_web.login"))

            if "Administrador total" in current_user.roles:
                return f(*args, **kwargs)

            path_actual = request.path

            if not current_user.paths:
                FlashMessages.flash_info("El usuario actual no tiene rutas asignadas")
                return redirect(url_for("home_template.index"))

            user_paths = [p.rstrip("/") for p in current_user.paths]

            if not any(path_actual.startswith(p) for p in user_paths):
                FlashMessages.flash_error("No tienes acceso a esta ruta")
                return redirect(url_for("home_template.index"))

            return f(*args, **kwargs)

        return decorated_function
    return decorator