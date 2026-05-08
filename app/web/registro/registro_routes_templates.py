from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.registro.registro_service import Registro_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.ruta.ruta_service import Ruta_Service
from app.extensions.db import db

registro_template_bp = Blueprint(
    "registro_template",
    __name__,
    template_folder="../../templates"
)

""" No se tienen templates para esta tabla, se estará trabajando desde editarProgramacion.html """