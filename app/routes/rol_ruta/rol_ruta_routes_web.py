from flask import Blueprint, render_template, abort, request, redirect, session, url_for, flash, get_flashed_messages
from flask_login import logout_user, login_required

# Extensions
from app.api.rol.rol_service import Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.extensions.messages import FlashMessages

# Services
from app.api.usuario.usuario_service import Usuario_Service
from app.api.rol_ruta.rol_ruta_service import Rol_Ruta_Service
from app.api.departamento.departamento_service import Departamento_Service

rol_ruta_web_bp = Blueprint(
    "rol_ruta_web", 
    __name__, 
    template_folder="../../templates"
)

@rol_ruta_web_bp.route("/crearRol_Ruta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol_ruta.crear")
def crearRol_Ruta_web():
    if request.method == "POST":
        data = {
            "idRol": request.form.get("idRol"),
            "idRuta": request.form.get("idRuta"),
        }

        result = Rol_Ruta_Service.createRol_Ruta_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
                ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
                ))

    return redirect(url_for(
        "rol_template.crearUsuario_template",
        ))

@rol_ruta_web_bp.route("/editarRol_Ruta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol_ruta.editar")
def editarRol_Ruta_web():
    if request.method == "POST":
        data = {
            "idRol": request.form.get("idRol"),
            "idRuta": request.form.get("idRuta"),
        }

        result = Usuario_Service.updateUsuario_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "rol_template.listaRoles_template", 
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "rol_template.listaRoles_template", 
            ))

    return redirect(url_for(
        "rol_template.listaRoles_template", 
    ))    

@rol_ruta_web_bp.route("/eliminarRol_Ruta_web", methods=["GET", "POST"])
@login_required
@permiso_requerido("rol_ruta.eliminar")
def eliminarRol_Ruta_web():
    if request.method == "POST":
        data = {
            "idRol": request.form.get("idRol"),
            "idRuta": request.form.get("idRuta"),
        }

        result = Rol_Ruta_Service.deleteRol_Ruta_service(db, data)

        if "error" in result:
            FlashMessages.flash_error(result["error"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
            ))
        else:
            FlashMessages.flash_success(result["mensaje"])
            return redirect(url_for(
                "rol_template.listaRoles_template",
            ))

    return redirect(url_for(
        "rol_template.listaRoles_template", 
    ))    