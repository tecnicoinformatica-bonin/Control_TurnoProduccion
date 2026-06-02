from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.motivo_desasignacion.motivo_desasignacion_service import Motivo_desasignacion_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

motivo_desasignacion_template_bp = Blueprint(
    "motivo_desasignacion_template",
    __name__,
    template_folder="../../templates"
)

@motivo_desasignacion_template_bp.route("/crearMotivo_desasignacion")
@login_required
@permiso_requerido("motivo_desasignacion.crear")
def crearMotivo_desasignacion_template():
    motivos_desasignacion = Motivo_desasignacion_Service.getMotivos_desasignacion_service(db)

    return render_template(
        f"motivo_desasignacion/crearMotivo_desasignacion.html", 
        motivos_desasignacion = motivos_desasignacion,
    )

@motivo_desasignacion_template_bp.route("/listaMotivos_desasignacion")
@login_required
@permiso_requerido("motivo_desasignacion.ver")
def listaMotivos_desasignacion_template():
    motivos_desasignacion = Motivo_desasignacion_Service.getMotivos_desasignacion_service(db)
            
    return render_template(
        f"motivo_desasignacion/listaMotivos_desasignacion.html", 
        motivos_desasignacion = motivos_desasignacion,
    )

