from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

from app.api.permiso.permiso_service import Permiso_Service
from app.api.usuario.usuario_service import Usuario_Service
from app.api.rol.rol_service import Rol_Service
from app.api.usuario_permiso.usuario_permiso_service import Usuario_Permiso_Service
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.core.auth.rbca_decorator import ruta_requerida
from app.extensions.db import db
from app.extensions.messages import FlashMessages

usuario_template_bp = Blueprint(
    "usuario_template",
    __name__,
    template_folder="../../templates"
)

@usuario_template_bp.route("/login")
def login():
    return render_template("usuario/login.html")

@usuario_template_bp.route("/crearUsuario")
@login_required
@ruta_requerida()
def crearUsuario_template():
    usuarios = Usuario_Service.getUsuarios_service(db)
    roles = Rol_Service.getRoles_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
        
    return render_template(
        f"usuario/crearUsuario.html", 
        usuarios = usuarios,
        roles = roles,
        usuario_roles = usuario_roles,
    )

@usuario_template_bp.route("/listaUsuarios")
@login_required
def listaUsuarios_template():
    usuarios = Usuario_Service.getUsuarios_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    usuario_permisos = Usuario_Permiso_Service.getUsuario_Permisos_service(db)
    roles = Rol_Service.getRoles_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
            
    return render_template(
        f"usuario/listaUsuarios.html", 
        usuarios = usuarios,
        roles = roles,
        usuario_roles = usuario_roles,
        permisos = permisos,
        usuario_permisos = usuario_permisos,
    )

