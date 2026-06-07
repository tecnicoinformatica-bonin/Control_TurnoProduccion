from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required

from app.api.autorizacion.autorizacion_service import Autorizacion_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.usuario.usuario_repository import UsuarioRepository
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

autorizacion_template_bp = Blueprint(
    "autorizacion_template",
    __name__,
    template_folder="../../templates"
)

@autorizacion_template_bp.route("/autorizacion_horas")
@login_required
# @permiso_requerido("autorizacion.ver")
def autorizacion_horas_template():
    autorizaciones = Autorizacion_Service.getAutorizaciones_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)

    departamentos_usuario = UsuarioRepository.getUserDepartmentsById(db, current_user.id)

    idDepartment = 0
    for d in departamentos_usuario:
        idDepartment = d["idDepartment"]
            
    return render_template(
        f"autorizacion/autorizacion_horas.html", 
        autorizaciones = autorizaciones,
        departamentos = departamentos,
        idDepartment = idDepartment,
    )