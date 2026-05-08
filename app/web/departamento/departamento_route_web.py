from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.extensions.db import db
from app.extensions.messages import FlashMessages

from app.api.departamento.departamento_service import Departamento_Service

departamento_web_bp = Blueprint(
    "departamento_web",
    __name__
)

@departamento_web_bp.route("/crearDepartamento_web", methods=["GET", "POST"])
@login_required
def crearDepartamento_web():
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "aplica_horas_extra": request.form.get("aplica_horas_extra"),
        }

        result = Departamento_Service.createDepartamento_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("departamento_template.crearDepartamento_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("departamento_template.crearDepartamento_template"))

    return redirect(url_for("departamento/crearDepartamento.html"))    

@departamento_web_bp.route("/editarDepartamento_web", methods=["GET", "POST"])
@login_required
def editarDepartamento_web():
    if request.method == "POST":
        data = {
            "idDepartment": request.form.get("idDepartment"),
            "name": request.form.get("name"),
            "aplica_horas_extra": request.form.get("aplica_horas_extra"),
        }

        result = Departamento_Service.updateDepartamento_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("departamento_template.listaDepartamentos_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("departamento_template.listaDepartamentos_template"))

    return redirect(url_for("departamento_template.listaDepartamentos_template"))

@departamento_web_bp.route("/eliminarDepartamento_web", methods=["GET", "POST"])
@login_required
def eliminarDepartamento_web():
    if request.method == "POST":
        data = {
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Departamento_Service.deleteDepartamento_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("departamento_template.listaDepartamentos_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("departamento_template.listaDepartamentos_template"))

    return redirect(url_for("departamento_template.listaDepartamentos_template"))