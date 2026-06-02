from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

registro_motivo_desasignacion_template_bp = Blueprint(
    "registro_motivo_desasignacion_template",
    __name__,
    template_folder="../../templates"
)

