from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user

# Extensions
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

from app.api.programacion.programacion_service import Programacion_Service

programacion_web_bp = Blueprint(
    "programacion_web",
    __name__
)

@programacion_web_bp.route("/crearProgramacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.crear")
def crearProgramacion_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)

    if request.method == "POST":
        data = {
            "fecha": request.form.get("fecha"),
            "idDepartment": request.form.get("idDepartment"),
        }

        result = Programacion_Service.createProgramacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("programacion_template.crearProgramacion_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("programacion_template.crearProgramacion_template"))

    return redirect(url_for(
        "programacion_template.crearProgramacion_template", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
        ))    

@programacion_web_bp.route("/crearProgramacionAutomatica_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.crear")
def crearProgramacionAutomatica_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)

    if request.method == "POST":
        data = {
            "fecha": request.form.get("fecha"),
        }

        result = Programacion_Service.createProgramacionAutomatica_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("home_template.index"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("home_template.index"))

    return redirect(url_for(
        "home_template.index", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
        ))    

@programacion_web_bp.route("/crearProgramacionPorDepartamentosUsuario_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.crear")
def crearProgramacionPorDepartamentosUsuario_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)

    if request.method == "POST":
        data = {
            "fecha": request.form.get("fecha"),
            "elaborado_por": request.form.get("elaborado_por"),
            "departamentos": request.form.getlist("departamentos"),
        }

        departamentos_usuario = [
            str(d["idDepartment"])
            for d in current_user.departamentos
        ]

        for depto in data["departamentos"]:
            if depto not in departamentos_usuario:
                FlashMessages.flash_error(
                    "Intento de acceso no autorizado."
                )

                return redirect(url_for("home_template.index"))

        result = Programacion_Service.crearProgramacionPorDepartamentosUsuario(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("home_template.index"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("home_template.index"))

    return redirect(url_for(
        "home_template.index", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
        )
    )

@programacion_web_bp.route("/cerrarProgramacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.editar")
def cerrarProgramacion_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)
    
    if request.method == "POST":
        data = {
            "idProgramacion": request.form.get("idProgramacion"),
            "fecha": request.form.get("fecha"),
            "fecha_cierre": request.form.get("fecha_cierre"),
            "idDepartment": request.form.get("idDepartment"),
            "elaborado_por": request.form.get("elaborado_por"),
            "cerrado_por": request.form.get("cerrado_por"),
            "estado": request.form.get("estado"),
        }
        fecha = data['fecha']
        idDepartment = data['idDepartment']

        result = Programacion_Service.cerrarProgramacion_service(db, data)

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
                programaciones = programaciones,
                programaciones_borrador = programaciones_borrador,
                ))

    return redirect(url_for(
        "programacion_template.editarProgramacion_template", 
        fecha = fecha,
        idDepartment = idDepartment,
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
    ))    

@programacion_web_bp.route("/reOpenProgramacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.editar")
def reOpenProgramacion_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)
    
    if request.method == "POST":
        data = {
            "fecha": request.form.get("fecha"),
            "idDepartment": request.form.get("idDepartment"),
            "reabierto_por": request.form.get("reabierto_por"),
            "motivo_reapertura": request.form.get("motivo_reapertura"),
        }

        result = Programacion_Service.reOpenProgramacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("programacion_template.listaProgramaciones_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "programacion_template.listaProgramaciones_template",
                programaciones = programaciones,
                programaciones_borrador = programaciones_borrador,
                ))

    return redirect(url_for(
        "programacion_template.listaProgramaciones_template", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
    ))    

@programacion_web_bp.route("/eliminarProgramacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.eliminar")
def eliminarProgramacion_web():
    programaciones = Programacion_Service.getProgramaciones_service(db)
    programaciones_borrador = Programacion_Service.getProgramacionesEnBorrador_service(db)

    if request.method == "POST":
        data = {
            "idProgramacion": request.form.get("idProgramacion"),
        }

        result = Programacion_Service.deleteProgramacion_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for("programacion_template.listaProgramaciones_template"))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for("programacion_template.listaProgramaciones_template"))

    return redirect(url_for(
        "programacion_template.listaProgramaciones_template", 
        programaciones = programaciones,
        programaciones_borrador = programaciones_borrador,
    ))

@programacion_web_bp.route("/confirmar_verificacion_programacion_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("programacion.confirmarAsignaciones")
def confirmar_verificacion_programacion_web():
    if request.method == "POST":
        data = {
            "idProgramacion": request.form.get("idProgramacion"),
            "verificado_por": request.form.get("verificado_por"),
            "fecha": request.form.get("fecha"),
            "idDepartment": request.form.get("idDepartment"),
        }
        fecha = data['fecha']
        idDepartment = data['idDepartment']

        result = Programacion_Service.confirmar_verificacion_programacion_service(db, data)

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
