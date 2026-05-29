from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required

# Extensions
from app.api.departamento.departamento_service import Departamento_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages
from app.extensions.date_parse import parse_fecha
from app.api.registro.registro_service import Registro_Service

registro_web_bp = Blueprint(
    "registro_web",
    __name__
)

@registro_web_bp.route("/crearRegistro_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("registro.crear")
def crearRegistro_web():
    if request.method == "POST":
        data = {
            "idProgramacion": request.form.get("idProgramacion"),
            "idEmpleado": request.form.get("idEmpleado"),
            "hora_inicio": parse_fecha(request.form.get("hora_inicio")),
            "hora_fin": parse_fecha(request.form.get("hora_fin")),
            "idLinea": request.form.get("idLinea"),
            "idProceso": request.form.get("idProceso"),
            "aplica_almuerzo": request.form.get("aplica_almuerzo"),
            "aplica_cena": request.form.get("aplica_cena"),
            "aplica_transporte": request.form.get("aplica_transporte"),
            "observacion_transporte": request.form.get("observacion_transporte"),"idCentro": request.form.get("idCentro"),
        }

        programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, data['idProgramacion'])
        empleado = Empleado_Service.getEmpleadoById_service(db, data['idEmpleado'])

        data["fecha"] = fecha = programacion['fecha']
        data["idCentro"] = empleado['idCentro']
        data["badgeNumber"] = empleado['idCentro']
        idDepartment = programacion['idDepartment']

        result = Registro_Service.createRegistro_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))

    return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))

@registro_web_bp.route("/editarRegistro_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("registro.editar")
def editarRegistro_web():
    if request.method == "POST":
        data = {
            "idRegistro": request.form.get("idRegistro"),
            "idEmpleado": request.form.get("idEmpleado"),
            "hora_inicio": request.form.get("hora_inicio"),
            "hora_fin": request.form.get("hora_fin"),
            "idLinea": request.form.get("idLinea"),
            "idProceso": request.form.get("idProceso"),
            "aplica_almuerzo": request.form.get("aplica_almuerzo"),
            "aplica_cena": request.form.get("aplica_cena"),
            "aplica_transporte": request.form.get("aplica_transporte"),
            "observacion_transporte": request.form.get("observacion_transporte"),
        }

        registro_actual = Registro_Service.getRegistroById_service(db, data['idRegistro'])
        programacion_actual = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro_actual['idProgramacion'])
        empleado = Empleado_Service.getEmpleadoById_service(db, data['idEmpleado'])

        data["fecha"] = fecha = programacion_actual['fecha']
        data["idCentro"] = empleado['idCentro']
        data["badgeNumber"] = empleado['idCentro']
        idDepartment = programacion_actual['idDepartment']

        result = Registro_Service.updateRegistro_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))

    return redirect(url_for(
        "programacion_template.editarProgramacion_template",
        fecha = fecha,
        idDepartment = idDepartment,
    ))    

@registro_web_bp.route("/eliminarRegistro_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("registro.eliminar")
def eliminarRegistro_web():
    if request.method == "POST":
        data = {
            "idRegistro": request.form.get("idRegistro"),
        }

        registro_actual = Registro_Service.getRegistroById_service(db, data['idRegistro'])
        programacion_actual = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro_actual['idProgramacion'])
        fecha = programacion_actual['fecha']
        idDepartment = programacion_actual['idDepartment']

        result = Registro_Service.deleteRegistro_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "programacion_template.editarProgramacion_template",
                fecha = fecha,
                idDepartment = idDepartment,
            ))

    return redirect(url_for(
        "programacion_template.editarProgramacion_template",
        fecha = fecha,
        idDepartment = idDepartment,
    ))    