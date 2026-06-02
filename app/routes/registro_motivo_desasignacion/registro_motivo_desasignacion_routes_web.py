from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

registro_motivo_desasignacion_web_bp = Blueprint(
    "registro_motivo_desasignacion_web",
    __name__
)

