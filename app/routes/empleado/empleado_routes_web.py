from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

from app.api.empleado.empleado_service import Empleado_Service

empleado_web_bp = Blueprint(
    "empleado_web",
    __name__
)

@empleado_web_bp.route("/crearEmpleado_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("empleado.crear")
def crearEmpleado_web():
    if request.method == "POST":
        data = {
            "idEmpleado": request.form.get("idEmpleado"),
            "badgeNumber": request.form.get("badgeNumber"),
            "firstName": request.form.get("firstName"),
            "secondName": request.form.get("secondName"),
            "lastName": request.form.get("lastName"),
            "lastName2": request.form.get("lastName2"),
            "position": request.form.get("position"),
            "idDepartment": request.form.get("idDepartment"),
            "activo": request.form.get("activo"),
            "idCentro": request.form.get("idCentro"),
            "idLinea": request.form.get("idLinea"),
            "idProceso": request.form.get("idProceso"),
            "idHorario": request.form.get("idHorario"),
        }

        result = Empleado_Service.createEmpleado_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("empleado_template.crearEmpleado_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("empleado_template.crearEmpleado_template"))

    return redirect(url_for("empleado_template.crearEmpleado_template"))    

@empleado_web_bp.route("/editarEmpleado_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("empleado.editar")
def editarEmpleado_web():
    if request.method == "POST":
        data = {
            "idEmpleado": request.form.get("idEmpleado"),
            "badgeNumber": request.form.get("badgeNumber"),
            "firstName": request.form.get("firstName"),
            "secondName": request.form.get("secondName"),
            "lastName": request.form.get("lastName"),
            "lastName2": request.form.get("lastName2"),
            "position": request.form.get("position"),
            "idDepartment": request.form.get("idDepartment"),
            "activo": request.form.get("activo"),
            "idCentro": request.form.get("idCentro"),
            "idLinea": request.form.get("idLinea"),
            "idProceso": request.form.get("idProceso"),
            "oldIdEmpleado": request.form.get("oldIdEmpleado"),
            "idHorario": request.form.get("idHorario"),
            "oldBadgeNumber": request.form.get("oldBadgeNumber"),
        }

        result = Empleado_Service.updateEmpleado_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("empleado_template.listaEmpleados_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("empleado_template.listaEmpleados_template"))

    return redirect(url_for("empleado_template.listaEmpleados_template"))    

@empleado_web_bp.route("/eliminarEmpleado_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("empleado.eliminar")
def eliminarEmpleado_web():
    if request.method == "POST":
        data = {
            "idEmpleado": request.form.get("idEmpleado"),
        }

        result = Empleado_Service.deleteEmpleado_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("empleado_template.listaEmpleados_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("empleado_template.listaEmpleados_template"))

    return redirect(url_for("empleado_template.listaEmpleados_template"))    