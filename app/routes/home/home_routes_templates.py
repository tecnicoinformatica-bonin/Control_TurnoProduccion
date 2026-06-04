from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from datetime import datetime

from app.api.departamento.departamento_service import Departamento_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.rol.rol_service import Rol_Service
from app.api.usuario.usuario_repository import UsuarioRepository
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.extensions.db import db

home_template_bp = Blueprint(
    "home_template",
    __name__,
    template_folder="../../templates"
)

@home_template_bp.route("/home")
@login_required
def index():
    departamentos = Departamento_Service.getDepartamentos_service(db)
    departamentos_aplica_horas_extra = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)
    roles = Rol_Service.getRoles_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesActivas_service(db)
    programaciones = Programacion_Service.getProgramaciones_service(db)
    fecha_actual = datetime.now()

    departamentos_usuario = UsuarioRepository.getUserDepartmentsById(db, current_user.id)

    idDepartment = 0
    for d in departamentos_usuario:
        idDepartment = d["idDepartment"]

    dept = 0
    for d in departamentos_aplica_horas_extra:
        dept = d['idDepartment']
    
    return render_template(
        "home/home.html", 
        departamentos = departamentos,
        departamentos_aplica_horas_extra = departamentos_aplica_horas_extra,
        roles = roles,
        usuario_roles = usuario_roles,
        fecha_actual = fecha_actual,
        programaciones_borrador = programaciones_borrador,
        dept = dept,
        programaciones = programaciones,
        idDepartment = idDepartment,
        )