from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import logout_user, login_required

# Extensions
from app.api.permiso.permiso_service import Permiso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service
from app.api.usuario_permiso.usuario_permiso_service import Usuario_Permiso_Service

usuario_permiso_web_bp = Blueprint(
    "usuario_permiso_web", 
    __name__, 
    template_folder="../../templates"
)

@usuario_permiso_web_bp.route("/crearUsuario_Permiso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario_permiso.crear")
def crearUsuario_Permiso_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idPermiso": request.form.get("idPermiso"),
        }

        result = Usuario_Permiso_Service.createUsuario_Permiso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
                ))

    return redirect(url_for(
        "usuario_template.crearUsuario_template",
        ))

@usuario_permiso_web_bp.route("/editarUsuario_Permiso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario_permiso.editar")
def editarUsuario_Permiso_web():
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
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template", 
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
    ))    

@usuario_permiso_web_bp.route("/eliminarUsuario_Permiso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario_permiso.eliminar")
def eliminarUsuario_Permiso_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idPermiso": request.form.get("idPermiso"),
        }

        result = Usuario_Permiso_Service.deleteUsuario_Permiso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "usuario_template.listaUsuarios_template",
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
    ))    