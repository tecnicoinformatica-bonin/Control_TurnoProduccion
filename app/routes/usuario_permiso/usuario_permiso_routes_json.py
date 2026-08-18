
from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.api.usuario_permiso.usuario_permiso_service import Usuario_Permiso_Service

from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_permiso_json_bp = Blueprint("usuario_permiso_json_pb", __name__)

@usuario_permiso_json_bp.route("/create_usuario_permiso_con_duplicados", methods=["POST"])
@login_required
@permiso_requerido("usuario_permiso.crear")
def create_usuario_permiso_con_duplicados():
    try:
        data = request.get_json()
        contador = 0
            
        if not data:
            return {
                "success": False
            }, 400
    
        for row in data:
            if row["asignado"]:
                Usuario_Permiso_Service.create_usuario_permiso_con_duplicados_service(db, row["idUsuario"], row["idPermiso"])
                contador += 1
    
            if (
                Usuario_Permiso_Service.exists_usuario_permiso(db, row["idUsuario"], row["idPermiso"])
                and not row["asignado"]
            ):
                dataExists = {
                    "idUsuario": row["idUsuario"],
                    "idPermiso": row["idPermiso"],
                }
                Usuario_Permiso_Service.deleteUsuario_Permiso_service(db, dataExists)
    
        return {
            "success": True,
            "usuario_permisos_creados": contador
        }, 201
    except Exception as ex:
        return {
            "success": False,
            "error": str(ex)
        }, 201
    