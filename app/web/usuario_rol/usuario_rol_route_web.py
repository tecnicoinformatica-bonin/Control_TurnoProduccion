from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import logout_user, login_required

# Extensions
from app.api.rol.rol_service import Rol_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.api.departamento.departamento_service import Departamento_Service

usuario_rol_web_bp = Blueprint(
    "usuario_rol_web", 
    __name__, 
    template_folder="../../templates"
)

@usuario_rol_web_bp.route("/crearUsuario_Rol_web", methods=["GET", "POST"])
@login_required
def crearUsuario_Rol_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    roles = Rol_Service.getRoles_service(db)

    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idRol": request.form.get("idRol"),
        }

        result = Usuario_Rol_Service.createUsuario_Rol_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                usuarios = usuarios,
                roles = roles,
                usuario_roles = usuario_roles,
                ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                usuarios = usuarios,
                roles = roles,
                usuario_roles = usuario_roles,
                ))

    return redirect(url_for(
        "usuario_template.crearUsuario_template",
        usuarios = usuarios,
        roles = roles,
        usuario_roles = usuario_roles,
        ))

@usuario_rol_web_bp.route("/editarUsuario_Rol_web", methods=["GET", "POST"])
@login_required
def editarUsuario_Rol_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)
    roles = Rol_Service.getRoles_service(db)

    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "username": request.form.get("username"),
            "nombre": request.form.get("nombre"),
            "password": request.form.get("password"),
            "activo": request.form.get("activo"),
        }

        result = Usuario_Service.updateUsuario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template", 
                usuarios = usuarios, 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template", 
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
        usuarios = usuarios,
    ))    

@usuario_rol_web_bp.route("/eliminarUsuario_Rol_web", methods=["GET", "POST"])
@login_required
def eliminarUsuario_Rol_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    roles = Rol_Service.getRoles_service(db)
    
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idRol": request.form.get("idRol"),
        }

        result = Usuario_Rol_Service.deleteUsuario_Rol_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                usuarios = usuarios,
                roles = roles,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                usuarios = usuarios,
                roles = roles,
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
        usuarios = usuarios,
        roles = roles,
    ))    