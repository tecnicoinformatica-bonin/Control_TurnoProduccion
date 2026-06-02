from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.motivo_desasignacion.motivo_desasignacion_service import Motivo_desasignacion_Service

motivo_desasignacion_web_bp = Blueprint(
    "motivo_desasignacion_web",
    __name__
)

@motivo_desasignacion_web_bp.route("/crearMotivo_desasignacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("motivo_desasignacion.crear")
def crearMotivo_desasignacion_web():
    if request.method == "POST":
        data = {
            "descripcion": request.form.get("descripcion"),
        }

        result = Motivo_desasignacion_Service.createMotivo_desasignacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("motivo_desasignacion_template.crearMotivo_desasignacion_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("motivo_desasignacion_template.crearMotivo_desasignacion_template"))

    return redirect(url_for("motivo_desasignacion_template.crearMotivo_desasignacion_template",))

@motivo_desasignacion_web_bp.route("/editarMotivo_desasignacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("motivo_desasignacion.editar")
def editarMotivo_desasignacion_web():
    if request.method == "POST":
        data = {
            "idMotivo": request.form.get("idMotivo"),
            "descripcion": request.form.get("descripcion"),
        }

        result = Motivo_desasignacion_Service.updateMotivo_desasignacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "motivo_desasignacion_template.listaMotivos_desasignacion_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "motivo_desasignacion_template.listaMotivos_desasignacion_template", 
            ))

    return redirect(url_for(
        "motivo_desasignacion_template.listaMotivos_desasignacion_template", 
    ))    

@motivo_desasignacion_web_bp.route("/eliminarMotivo_desasignacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("motivo_desasignacion.eliminar")
def eliminarMotivo_desasignacion_web():
    if request.method == "POST":
        data = {
            "idMotivo": request.form.get("idMotivo"),
        }

        result = Motivo_desasignacion_Service.deleteMotivo_desasignacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "motivo_desasignacion_template.listaMotivos_desasignacion_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "motivo_desasignacion_template.listaMotivos_desasignacion_template",
            ))

    return redirect(url_for(
        "motivo_desasignacion_template.listaMotivos_desasignacion_template", 
    ))    