from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from datetime import datetime

from app.api.departamento.departamento_service import Departamento_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.rol.rol_service import Rol_Service
from app.api.usuario.usuario_repository import UsuarioRepository
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

estadisticas_template_bp = Blueprint(
    "estadisticas_template",
    __name__,
    template_folder="../../templates"
)

@estadisticas_template_bp.route("/estadisticas/<string:from_date>/<string:to_date>/<int:idDepartment>")
@login_required
@permiso_requerido("estadisticas.ver")
def estadisticas_template(from_date, to_date, idDepartment):

    idDepartment_value = idDepartment
    from_date_value = from_date
    to_date_value = to_date
    
    return render_template(
        "estadisticas/estadisticas.html", 
        idDepartment_value = idDepartment_value,
        from_date_value = from_date_value,
        to_date_value = to_date_value,
    )

@estadisticas_template_bp.route("/parametros_estadisticas")
@login_required
@permiso_requerido("estadisticas.ver")
def parametros_estadisticas_template():
    departamentos = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)
    departamentos_usuario = UsuarioRepository.getUserDepartmentsById(db, current_user.id)
        
    return render_template(
        f"estadisticas/parametros_estadisticas.html", 
        departamentos = departamentos,
        departamentos_usuario = departamentos_usuario,
    )