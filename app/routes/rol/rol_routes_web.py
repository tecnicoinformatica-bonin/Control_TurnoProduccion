from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.rol.rol_service import Rol_Service

rol_web_bp = Blueprint(
    "rol_web",
    __name__
)

@rol_web_bp.route("/crearRol_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol.crear")
def crearRol_web():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion"),
        }

        result = Rol_Service.createRol_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("rol_template.crearRol_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("rol_template.crearRol_template"))

    return redirect(url_for("rol_template.crearRol_template"))

@rol_web_bp.route("/editarRol_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol.editar")
def editarRol_web():
    if request.method == "POST":
        data = {
            "idRol": request.form.get("idRol"),
            "nombre": request.form.get("nombre"),
            "descripcion": request.form.get("descripcion"),
        }

        result = Rol_Service.updateRol_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "rol_template.listaRoles_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "rol_template.listaRoles_template", 
            ))

    return redirect(url_for(
        "rol_template.listaRoles_template", 
    ))    

@rol_web_bp.route("/eliminarRol_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol.eliminar")
def eliminarRol_web():
    if request.method == "POST":
        data = {
            "idRol": request.form.get("idRol"),
        }

        result = Rol_Service.deleteRol_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
            ))

    return redirect(url_for(
        "rol_template.listaRoles_template", 
    ))    