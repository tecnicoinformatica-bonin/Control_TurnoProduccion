
from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service

from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_rol_json_bp = Blueprint("usuario_rol_json_pb", __name__)

@usuario_rol_json_bp.route("/create_usuario_rol_con_duplicados", methods=["POST"])
@login_required
@permiso_requerido("usuario_rol.crear")
def create_usuario_rol_con_duplicados():
    try:
        data = request.get_json()
        contador = 0
            
        if not data:
            return {
                "success": False
            }, 400
    
        for row in data:
            if row["asignado"]:
                Usuario_Rol_Service.create_usuario_rol_con_duplicados_service(db, row["idUsuario"], row["idRol"])
                contador += 1
    
            if (
                Usuario_Rol_Service.exists_usuario_rol(db, row["idUsuario"], row["idRol"])
                and not row["asignado"]
            ):
                dataExists = {
                    "idUsuario": row["idUsuario"],
                    "idRol": row["idRol"],
                }
                Usuario_Rol_Service.deleteUsuario_Rol_service(db, dataExists)
    
        return {
            "success": True,
            "usuario_roles_creados": contador
        }, 201
    except Exception as ex:
        return {
            "success": False,
            "error": str(ex)
        }, 201
    