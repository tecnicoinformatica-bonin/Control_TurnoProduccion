from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.departamento.departamento_service import Departamento_Service
from app.api.importacion.importacion_service import Importacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

importacion_template_bp = Blueprint(
    "importacion_template",
    __name__,
    template_folder="../../templates"
)

@importacion_template_bp.route("/crearImportacion")
@login_required
@permiso_requerido("importacion.crear")
def crearImportacion_template():

    return render_template(
        f"importacion/crearImportacion.html", 
    )

@importacion_template_bp.route("/listaImportaciones")
@login_required
@permiso_requerido("importacion.ver")
def listaImportaciones_template():
    importaciones = Importacion_Service.getImportaciones_service(db)
            
    return render_template(
        f"importacion/listaImportaciones.html", 
        importaciones = importaciones,
    )

