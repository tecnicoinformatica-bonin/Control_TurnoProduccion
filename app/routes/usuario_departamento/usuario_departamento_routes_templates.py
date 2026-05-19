from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

from app.api.usuario.usuario_service import Usuario_Service
from app.api.usuario_departamento.usuario_departamento_service import Usuario_Departamento_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages

usuario_departamento_template_bp = Blueprint(
    "usuario_departamento_template",
    __name__,
    template_folder="../../templates"
)

""" Los templates para esta tabla se manejaron por medio de modales en el /templates/listaUsuario.html """