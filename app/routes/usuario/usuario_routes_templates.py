from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

from app.api.departamento.departamento_service import Departamento_Service
from app.api.permiso.permiso_service import Permiso_Service
from app.api.usuario.usuario_service import Usuario_Service
from app.api.rol.rol_service import Rol_Service
from app.api.usuario_departamento.usuario_departamento_model import Usuario_Departamento
from app.api.usuario_departamento.usuario_departamento_service import Usuario_Departamento_Service
from app.api.usuario_permiso.usuario_permiso_service import Usuario_Permiso_Service
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
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

@usuario_template_bp.route("/change_password_template/<idUsuario>")
def change_password_template(idUsuario):
    idUsuarioData = idUsuario

    return render_template(
        "usuario/change_password.html",
        idUsuarioData = idUsuarioData
    )

@usuario_template_bp.route("/crearUsuario")
@login_required
@permiso_requerido("usuario.crear")
def crearUsuario_template():
    usuarios = Usuario_Service.getUsuarios_service(db)
    roles = Rol_Service.getRoles_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    usuario_permisos = Usuario_Permiso_Service.getUsuario_Permisos_service(db)
    usuario_departamentos = Usuario_Departamento_Service.getUsuario_Departamentos_service(db)
        
    return render_template(
        f"usuario/crearUsuario.html", 
        usuarios = usuarios,
        roles = roles,
        permisos = permisos,
        departamentos = departamentos,
        usuario_roles = usuario_roles,
        usuario_permisos = usuario_permisos,
        usuario_departamentos = usuario_departamentos,
    )

@usuario_template_bp.route("/listaUsuarios")
@login_required
@permiso_requerido("usuario.ver")
def listaUsuarios_template():
    usuarios = Usuario_Service.getUsuarios_service(db)
    roles = Rol_Service.getRoles_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
    usuario_permisos = Usuario_Permiso_Service.getUsuario_Permisos_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    usuario_departamentos = Usuario_Departamento_Service.getUsuario_Departamentos_service(db)
            
    return render_template(
        f"usuario/listaUsuarios.html", 
        usuarios = usuarios,
        roles = roles,
        permisos = permisos,
        departamentos = departamentos,
        usuario_permisos = usuario_permisos,
        usuario_roles = usuario_roles,
        usuario_departamentos = usuario_departamentos,
    )