from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import logout_user, login_required

# Extensions
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service
from app.api.departamento.departamento_service import Departamento_Service

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
def crearUsuario_web():
    usuarios = Usuario_Service.getUsuarios_service(db)

    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "nombre": request.form.get("nombre"),
            "password": request.form.get("password"),
            "activo": request.form.get("activo"),
        }

        result = Usuario_Service.createUsuario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("usuario_template.crearUsuario_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("usuario_template.crearUsuario_template"))

    return redirect(url_for("usuario_template.crearUsuario_template", usuarios = usuarios))

@usuario_web_bp.route("/editarUsuario_web", methods=["GET", "POST"])
@login_required
def editarUsuario_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    
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
                usuarios = usuarios,
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
        usuarios = usuarios,
    ))    

@usuario_web_bp.route("/eliminarUsuario_web", methods=["GET", "POST"])
@login_required
def eliminarUsuario_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
        }

        result = Usuario_Service.deleteUsuario_service(db, data)

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
                usuarios = usuarios,
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
        usuarios = usuarios,
    ))    


@usuario_web_bp.route("/cambiarPasswordUsuario_web", methods=["GET", "POST"])
@login_required
def cambiarPasswordUsuario_web():
    usuarios = Usuario_Service.getUsuarios_service(db)
    
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "password": request.form.get("password"), 
            "confirmedPassword": request.form.get("confirmedPassword"), 
        }

        result = Usuario_Service.updatePassword_service(db, data)

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
                usuarios = usuarios,
            ))

    return redirect(url_for(
        "usuario_template.listaUsuarios_template", 
        usuarios = usuarios,
    ))    