from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import logout_user, login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service
from app.api.usuario_departamento.usuario_departamento_service import Usuario_Departamento_Service

usuario_departamento_web_bp = Blueprint(
    "usuario_departamento_web", 
    __name__, 
    template_folder="../../templates"
)

@usuario_departamento_web_bp.route("/crearUsuario_Departamento_web", methods=["GET", "POST"])
@login_required
def crearUsuario_Departamento_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Usuario_Departamento_Service.createUsuario_Departamento_service(db, data)

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

@usuario_departamento_web_bp.route("/eliminarUsuario_Departamento_web", methods=["GET", "POST"])
@login_required
def eliminarUsuario_Departamento_web():
    if request.method == "POST":
        data = {
            "idUsuario": request.form.get("idUsuario"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Usuario_Departamento_Service.deleteUsuario_Departamento_service(db, data)

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