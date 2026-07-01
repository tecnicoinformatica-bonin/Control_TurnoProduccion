from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import current_user, logout_user, login_required

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service

usuario_web_bp = Blueprint(
    "usuario_web", 
    __name__, 
    template_folder="../../templates"
)

@usuario_web_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }

        result = Usuario_Service.login_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            """ flash(result["error"], "error") """
            return redirect(url_for("usuario_web.login"))
        
        if current_user.cambiar_password == 1:
            return redirect(url_for(
                "usuario_template.change_password_template",
                idUsuario = result["idUsuario"],
            ))
        
        return redirect(url_for("home_template.index"))
    
    return render_template("usuario/login.html")

@usuario_web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("usuario_template.login"))


@usuario_web_bp.route("/crearUsuario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario.crear")
def crearUsuario_web():
    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "nombre": request.form.get("nombre"),
            "password": request.form.get("password"),
            "activo": request.form.get("activo"),
            "scope_departamentos_global": request.form.get("scope_departamentos_global"),
            "scope_permisos_global": request.form.get("scope_permisos_global"),
        }

        result = Usuario_Service.createUsuario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("usuario_template.crearUsuario_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("usuario_template.crearUsuario_template"))

    return redirect(url_for("usuario_template.crearUsuario_template"))

@usuario_web_bp.route("/editarUsuario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario.editar")
def editarUsuario_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "username": request.form.get("username"),
            "nombre": request.form.get("nombre"),
            "password": request.form.get("password"),
            "activo": request.form.get("activo"),
            "scope_departamentos_global": request.form.get("scope_departamentos_global"),
            "scope_permisos_global": request.form.get("scope_permisos_global"),
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

@usuario_web_bp.route("/eliminarUsuario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("usuario.eliminar")
def eliminarUsuario_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
        }

        result = Usuario_Service.deleteUsuario_service(db, data)

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


@usuario_web_bp.route("/cambiarPasswordUsuario_web", methods=["GET", "POST"])
@login_required
# @permiso_requerido("usuario.editar")
def cambiarPasswordUsuario_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "password": request.form.get("password"), 
            "confirmedPassword": request.form.get("confirmedPassword"), 
        }

        cambiar_password = current_user.cambiar_password

        result = Usuario_Service.updatePassword_service(db, data)
        usuarioResult = result["resultado"]["resultado"]

        if cambiar_password == 1 or cambiar_password == True:
            if "error" in result:
                FlashMessages.flash_error(result["error"])
                return redirect(url_for(
                    "usuario_template.change_password_template",
                    idUsuario = usuarioResult
                ))
            else:
                FlashMessages.flash_success(result["mensaje"])
                return redirect(url_for(
                    "home_template.index",
                ))
        else:
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