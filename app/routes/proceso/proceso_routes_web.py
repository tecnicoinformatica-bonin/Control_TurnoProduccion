from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.proceso.proceso_service import Proceso_Service

proceso_web_bp = Blueprint(
    "proceso_web",
    __name__
)

@proceso_web_bp.route("/crearProceso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("proceso.crear")
def crearProceso_web():
    if request.method == "POST":
        data = {
            "proceso": request.form.get("proceso"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Proceso_Service.createProceso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("proceso_template.crearProceso_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("proceso_template.crearProceso_template"))

    return redirect(url_for("proceso_template.crearProceso_template"))

@proceso_web_bp.route("/editarProceso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("proceso.editar")
def editarProceso_web():
    if request.method == "POST":
        data = {
            "idProceso": request.form.get("idProceso"),
            "proceso": request.form.get("proceso"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Proceso_Service.updateProceso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "proceso_template.listaProcesos_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "proceso_template.listaProcesos_template", 
            ))

    return redirect(url_for(
        "proceso_template.listaProcesos_template", 
    ))    

@proceso_web_bp.route("/eliminarProceso_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("proceso.eliminar")
def eliminarProceso_web():
    if request.method == "POST":
        data = {
            "idProceso": request.form.get("idProceso"),
        }

        result = Proceso_Service.deleteProceso_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "proceso_template.listaProcesos_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "proceso_template.listaProcesos_template",
            ))

    return redirect(url_for(
        "proceso_template.listaProcesos_template", 
    ))    