from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.linea.linea_service import Linea_Service

linea_web_bp = Blueprint(
    "linea_web",
    __name__
)

@linea_web_bp.route("/crearLinea_web", methods=["GET", "POST"])
@login_required
def crearLinea_web():
    lineas = Linea_Service.getLineas_service(db)

    if request.method == "POST":
        data = {
            "nameLinea": request.form.get("nameLinea"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Linea_Service.createLinea_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("linea_template.crearLinea_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("linea_template.crearLinea_template"))

    return redirect(url_for("linea_template.crearLinea_template", lineas = lineas))

@linea_web_bp.route("/editarLinea_web", methods=["GET", "POST"])
@login_required
def editarLinea_web():
    lineas = Linea_Service.getLineas_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
    
    if request.method == "POST":
        data = {
            "idLinea": request.form.get("idLinea"),
            "nameLinea": request.form.get("nameLinea"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Linea_Service.updateLinea_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "linea_template.listaLineas_template", 
                lineas = lineas, 
                departamentos = departamentos,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "linea_template.listaLineas_template", 
                lineas = lineas,
                departamentos = departamentos,
            ))

    return redirect(url_for(
        "linea_template.listaLineas_template", 
        lineas = lineas,
        departamentos = departamentos,
    ))    

@linea_web_bp.route("/eliminarLinea_web", methods=["GET", "POST"])
@login_required
def eliminarLinea_web():
    lineas = Linea_Service.getLineas_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
    
    if request.method == "POST":
        data = {
            "idLinea": request.form.get("idLinea"),
        }

        result = Linea_Service.deleteLinea_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "linea_template.listaLineas_template",
                lineas = lineas,
                departamentos = departamentos,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "linea_template.listaLineas_template",
                lineas = lineas,
                departamentos = departamentos,
            ))

    return redirect(url_for(
        "linea_template.listaLineas_template", 
        lineas = lineas,
        departamentos = departamentos,
    ))    