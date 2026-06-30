from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

from app.api.calendario_feriados.calendario_feriados_service import Feriado_Service

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

feriado_web_bp = Blueprint(
    "feriado_web",
    __name__
)

@feriado_web_bp.route("/crearFeriado_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("feriado.crear")
def crearFeriado_web():
    if request.method == "POST":
        data = {
            "nameFeriado": request.form.get("nameFeriado"),
            "idDepartment": request.form.get("idDepartment"),
            "minimo_requerido": request.form.get("minimo_requerido"),
        }

        result = Feriado_Service.createFeriado_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("feriado_template.crearFeriado_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("feriado_template.crearFeriado_template"))

    return redirect(url_for("feriado_template.crearFeriado_template",))
