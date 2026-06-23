from datetime import datetime

from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required

from app.api.motivo_desasignacion.motivo_desasignacion_service import Motivo_desasignacion_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.registro.registro_service import Registro_Service
from app.api.rol.rol_service import Rol_Service
from app.api.usuario.usuario_repository import UsuarioRepository
from app.api.usuario.usuario_service import Usuario_Service
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

programacion_template_bp = Blueprint(
    "programacion_template",
    __name__,
    template_folder="../../templates"
)

@programacion_template_bp.route("/crearProgramacion")
@login_required
@permiso_requerido("programacion.crear")
def crearProgramacion_template():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)
        
    return render_template(
        f"programacion/crearProgramacion.html", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
    )

@programacion_template_bp.route("/listaProgramaciones")
@login_required
@permiso_requerido("programacion.ver")
def listaProgramaciones_template():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesActivas_service(db)
            
    return render_template(
        f"programacion/listaProgramaciones.html", 
        programaciones = programaciones,
        departamentos = departamentos,
        usuarios = usuarios,
        programaciones_borrador = programaciones_borrador,
    )

@programacion_template_bp.route("/editarProgramacion/<idDepartment>/<fecha>")
@login_required
@permiso_requerido("programacion.ver")
def editarProgramacion_template(idDepartment, fecha):
    programaciones = Programacion_Service.getProgramaciones_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesActivas_service(db)
    programacion_actual = Programacion_Service.getProgramacionByDateAndIdDepartment_service(db, fecha, idDepartment)
    conteo_lineas = Programacion_Service.getCountsByLine_service(db, programacion_actual["idProgramacion"], programacion_actual["idDepartment"])
    registros = Registro_Service.getRegistros_service(db)
    motivos = Motivo_desasignacion_Service.getMotivos_desasignacion_service(db)
            
    return render_template(
        f"programacion/editarProgramacion.html", 
        programaciones = programaciones,
        departamentos = departamentos,
        usuarios = usuarios,
        programaciones_borrador = programaciones_borrador,
        idDepartment = int(idDepartment), 
        fecha = fecha,
        programacion_actual = programacion_actual,
        conteo_lineas = conteo_lineas,
        registros = registros,
        motivos = motivos
    )

@programacion_template_bp.route("/programaciones_general")
@login_required
@permiso_requerido("programacion.ver")
def programaciones_general():
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
        "programacion/programaciones_general.html", 
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
