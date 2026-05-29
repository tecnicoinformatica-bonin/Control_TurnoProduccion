from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.api.ruta.ruta_service import Ruta_Service

ruta_web_bp = Blueprint(
    "ruta_web",
    __name__
)

@ruta_web_bp.route("/crearRuta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("ruta.crear")
def crearRuta_web():
    if request.method == "POST":
        data = {
            "nombre": request.form.get("nombre"),
            "path": request.form.get("path"),
        }

        result = Ruta_Service.createRuta_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("ruta_template.crearRuta_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("ruta_template.crearRuta_template"))

    return redirect(url_for("ruta_template.crearRuta_template"))

@ruta_web_bp.route("/editarRuta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("ruta.editar")
def editarRuta_web():
    if request.method == "POST":
        data = {
            "idRuta": request.form.get("idRuta"),
            "nombre": request.form.get("nombre"),
            "path": request.form.get("path"),
        }

        result = Ruta_Service.updateRuta_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "ruta_template.listaRutas_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "ruta_template.listaRutas_template", 
            ))

    return redirect(url_for(
        "ruta_template.listaRutas_template", 
    ))    

@ruta_web_bp.route("/eliminarRuta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("ruta.eliminar")
def eliminarRuta_web():
    if request.method == "POST":
        data = {
            "idRuta": request.form.get("idRuta"),
        }

        result = Ruta_Service.deleteRuta_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "ruta_template.listaRutas_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "ruta_template.listaRutas_template",
            ))

    return redirect(url_for(
        "ruta_template.listaRutas_template", 
    ))    