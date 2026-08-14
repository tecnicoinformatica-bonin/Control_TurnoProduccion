
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from datetime import datetime
import pytz

from app.api.rol_permiso.rol_permiso_service import Rol_Permiso_Service

from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

rol_permiso_json_bp = Blueprint("rol_permiso_json_pb", __name__)

@rol_permiso_json_bp.route("/create_rol_permiso_con_duplicados", methods=["POST"])
@login_required
@permiso_requerido("rol_permiso.crear")
def create_rol_permiso_con_duplicados():
    try:
        data = request.get_json()
        contador = 0
            
        if not data:
            return {
                "success": False
            }, 400
    
        for row in data:
            if row["asignado"]:
                Rol_Permiso_Service.create_rol_permiso_con_duplicados_service(db, row["idRol"], row["idPermiso"])
                contador += 1
    
            if (
                Rol_Permiso_Service.exists_rol_permiso(db, row["idRol"], row["idPermiso"])
                and not row["asignado"]
            ):
                dataExists = {
                    "idRol": row["idRol"],
                    "idPermiso": row["idPermiso"],
                }
                Rol_Permiso_Service.deleteRol_Permiso_service(db, dataExists)
    
        return {
            "success": True,
            "rol_permisos_creados": contador
        }, 201
    except Exception as ex:
        return {
            "success": False,
            "error": str(ex)
        }, 201
    