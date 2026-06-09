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

@autorizacion_template_bp.route("/autorizacion_horas/<string:from_date>/<string:to_date>/<int:idDepartment>")
@login_required
# @permiso_requerido("autorizacion.ver")
def autorizacion_horas_template(from_date, to_date, idDepartment):
    autorizaciones = Autorizacion_Service.getAutorizaciones_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)

    departamentos_usuario = UsuarioRepository.getUserDepartmentsById(db, current_user.id)
    
    idDepartment_value = idDepartment
    from_date_value = from_date
    to_date_value = to_date

    return render_template(
        f"autorizacion/autorizacion_horas.html", 
        autorizaciones = autorizaciones,
        departamentos = departamentos,
        idDepartment_value = idDepartment_value,
        from_date_value = from_date_value,
        to_date_value = to_date_value,
    )

@autorizacion_template_bp.route("/parametros_autorizacion_horas")
@login_required
# @permiso_requerido("autorizacion.ver")
def parametros_autorizacion_horas_template():
    departamentos = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)
    departamentos_usuario = UsuarioRepository.getUserDepartmentsById(db, current_user.id)
        
    return render_template(
        f"autorizacion/parametros_autorizacion_horas.html", 
        departamentos = departamentos,
        departamentos_usuario = departamentos_usuario,
    )