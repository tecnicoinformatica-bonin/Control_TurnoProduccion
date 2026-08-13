from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.permiso.permiso_service import Permiso_Service
from app.api.rol.rol_service import Rol_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.rol_permiso.rol_permiso_service import Rol_Permiso_Service
from app.api.usuario.usuario_service import Usuario_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

rol_template_bp = Blueprint(
    "rol_template",
    __name__,
    template_folder="../../templates"
)

@rol_template_bp.route("/crearRol")
@login_required
@permiso_requerido("rol.crear")
def crearRol_template():
    roles = Rol_Service.getRoles_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    rol_permisos = Rol_Permiso_Service.getRol_Permisos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
        
    return render_template(
        f"rol/crearRol.html", 
        roles = roles,
        permisos = permisos,
        rol_permisos = rol_permisos,
        usuarios = usuarios,
    )

@rol_template_bp.route("/listaRoles")
@login_required
@permiso_requerido("rol.ver")
def listaRoles_template():
    roles = Rol_Service.getRoles_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    rol_permisos = Rol_Permiso_Service.getRol_Permisos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
            
    return render_template(
        f"rol/listaRoles.html", 
        roles = roles,
        permisos = permisos,
        rol_permisos = rol_permisos,
        usuarios = usuarios,
    )

