from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service

centro_de_costo_web_bp = Blueprint(
    "centro_de_costo_web",
    __name__
)

@centro_de_costo_web_bp.route("/crearCentro_de_costo_web", methods=["GET", "POST"])
@login_required
def crearCentro_de_costo_web():
    if request.method == "POST":
        data = {
            "nombreCentro": request.form.get("nombreCentro"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Centro_de_costo_Service.createCentro_de_costo_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("centro_de_costo_template.crearCentro_de_costo_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("centro_de_costo_template.crearCentro_de_costo_template"))

    return redirect(url_for("centro_de_costo_template.crearCentro_de_costo_template"))

@centro_de_costo_web_bp.route("/editarCentro_de_costo_web", methods=["GET", "POST"])
@login_required
def editarCentro_de_costo_web():
    if request.method == "POST":
        data = {
            "idCentro": request.form.get("idCentro"),
            "nombreCentro": request.form.get("nombreCentro"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Centro_de_costo_Service.updateCentro_de_costo_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"            ))

    return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"))    

@centro_de_costo_web_bp.route("/eliminarCentro_de_costo_web", methods=["GET", "POST"])
@login_required
def eliminarCentro_de_costo_web():
    if request.method == "POST":
        data = {
            "idCentro": request.form.get("idCentro"),
        }

        result = Centro_de_costo_Service.deleteCentro_de_costo_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"))

    return redirect(url_for("centro_de_costo_template.listaCentros_de_costo_template"))    