from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.permiso.permiso_service import Permiso_Service

permiso_web_bp = Blueprint(
    "permiso_web",
    __name__
)

@permiso_web_bp.route("/crearPermiso_web", methods=["GET", "POST"])
@login_required
def crearPermiso_web():
    if request.method == "POST":
        data = {
            "nombrePermiso": request.form.get("nombrePermiso"),
            "descripcion": request.form.get("descripcion"),
        }

        result = Permiso_Service.createPermiso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("permiso_template.crearPermiso_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("permiso_template.crearPermiso_template"))

    return redirect(url_for("permiso_template.crearPermiso_template"))

@permiso_web_bp.route("/editarPermiso_web", methods=["GET", "POST"])
@login_required
def editarPermiso_web():
    if request.method == "POST":
        data = {
            "idPermiso": request.form.get("idPermiso"),
            "nombrePermiso": request.form.get("nombrePermiso"),
            "descripcion": request.form.get("descripcion"),
        }

        result = Permiso_Service.updatePermiso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("permiso_template.listaPermisos_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("permiso_template.listaPermisos_template"))

    return redirect(url_for("permiso_template.listaPermisos_template"))    

@permiso_web_bp.route("/eliminarPermiso_web", methods=["GET", "POST"])
@login_required
def eliminarPermiso_web():
    if request.method == "POST":
        data = {
            "idPermiso": request.form.get("idPermiso"),
        }

        result = Permiso_Service.deletePermiso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("permiso_template.listaPermisos_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("permiso_template.listaPermisos_template"))

    return redirect(url_for("permiso_template.listaPermisos_template"))    