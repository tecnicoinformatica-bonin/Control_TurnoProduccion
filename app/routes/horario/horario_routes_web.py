from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.horario.horario_service import Horario_Service

horario_web_bp = Blueprint(
    "horario_web",
    __name__
)

@horario_web_bp.route("/crearHorario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("horario.crear")
def crearHorario_web():
    if request.method == "POST":
        data = {
            "descripcionHorario": request.form.get("descripcionHorario"),
            "hora_inicio": request.form.get("hora_inicio"),
            "hora_fin": request.form.get("hora_fin"),
        }

        result = Horario_Service.createHorario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("horario_template.crearHorario_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("horario_template.crearHorario_template"))

    return redirect(url_for("horario_template.crearHorario_template",))

@horario_web_bp.route("/editarHorario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("horario.editar")
def editarHorario_web():
    if request.method == "POST":
        data = {
            "idHorario": request.form.get("idHorario"),
            "descripcionHorario": request.form.get("descripcionHorario"),
            "hora_inicio": request.form.get("hora_inicio"),
            "hora_fin": request.form.get("hora_fin")
        }

        result = Horario_Service.updateHorario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "horario_template.listaHorarios_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "horario_template.listaHorarios_template", 
            ))

    return redirect(url_for(
        "horario_template.listaHorarios_template", 
    ))    

@horario_web_bp.route("/eliminarHorario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("horario.eliminar")
def eliminarHorario_web():
    if request.method == "POST":
        data = {
            "idHorario": request.form.get("idHorario"),
        }

        result = Horario_Service.deleteHorario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "horario_template.listaHorarios_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "horario_template.listaHorarios_template",
            ))

    return redirect(url_for(
        "horario_template.listaHorarios_template", 
    ))    