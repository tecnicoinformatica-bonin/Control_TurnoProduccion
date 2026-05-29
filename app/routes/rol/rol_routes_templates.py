from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.permiso.permiso_service import Permiso_Service
from app.api.rol.rol_service import Rol_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.rol_permiso.rol_permiso_service import Rol_Permiso_Service
from app.api.rol_ruta.rol_ruta_service import Rol_Ruta_Service
from app.api.ruta.ruta_service import Ruta_Service
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
    rutas = Ruta_Service.getRutasDESC_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    rol_rutas = Rol_Ruta_Service.getRol_Rutas_service(db)
    rol_permisos = Rol_Permiso_Service.getRol_Permisos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
        
    return render_template(
        f"rol/crearRol.html", 
        roles = roles,
        rutas = rutas,
        permisos = permisos,
        rol_rutas = rol_rutas,
        rol_permisos = rol_permisos,
        usuarios = usuarios,
    )

@rol_template_bp.route("/listaRoles")
@login_required
@permiso_requerido("rol.ver")
def listaRoles_template():
    roles = Rol_Service.getRoles_service(db)
    rutas = Ruta_Service.getRutas_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    rol_rutas = Rol_Ruta_Service.getRol_Rutas_service(db)
    rol_permisos = Rol_Permiso_Service.getRol_Permisos_service(db)
    usuarios = Usuario_Service.getUsuarios_service(db)
            
    return render_template(
        f"rol/listaRoles.html", 
        roles = roles,
        rutas = rutas,
        permisos = permisos,
        rol_rutas = rol_rutas,
        rol_permisos = rol_permisos,
        usuarios = usuarios,
    )

