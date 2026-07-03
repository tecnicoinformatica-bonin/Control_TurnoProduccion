from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import current_user, login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

estadisticas_web_bp = Blueprint(
    "estadisticas_web",
    __name__
)

@estadisticas_web_bp.route("/parametros_estadisticas_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("estadisticas.ver")
def parametros_estadisticas_web():
    if request.method == "POST":
        data = {
            "idDepartment": request.form.get("idDepartment"),
            "from_date": request.form.get("from_date"),
            "to_date": request.form.get("to_date"),
        }

        idDepartment = int(data["idDepartment"])
        from_date = data["from_date"]
        to_date = data["to_date"]

        departamentos_usuario = {
            d["idDepartment"]
            for d in current_user.departamentos
        }

        if (
            idDepartment not in departamentos_usuario
            and current_user.scope_departamentos_global == 0
        ):
            FlashMessages.flash_error("No tiene permisos para ver ese departamento")
            return redirect(url_for("estadisticas_template.parametros_estadisticas_template"))

    return redirect(url_for(
        "estadisticas_template.estadisticas_template",
        idDepartment = idDepartment,
        from_date = from_date,
        to_date = to_date,
    ))