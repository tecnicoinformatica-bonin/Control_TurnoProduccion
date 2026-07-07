from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.configuracion.configuracion_service import Configuracion_Service

configuracion_web_bp = Blueprint(
    "configuracion_web",
    __name__
)

