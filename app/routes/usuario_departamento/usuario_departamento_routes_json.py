
from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.api.usuario_departamento.usuario_departamento_service import Usuario_Departamento_Service

from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_departamento_json_bp = Blueprint("usuario_departamento_json_pb", __name__)

@usuario_departamento_json_bp.route("/create_usuario_departamento_con_duplicados", methods=["POST"])
@login_required
@permiso_requerido("usuario_departamento.crear")
def create_usuario_departamento_con_duplicados():
    try:
        data = request.get_json()
        contador = 0
            
        if not data:
            return {
                "success": False
            }, 400
    
        for row in data:
            if row["asignado"]:
                Usuario_Departamento_Service.create_usuario_departamento_con_duplicados_service(db, row["idUsuario"], row["idDepartment"])
                contador += 1
    
            if (
                Usuario_Departamento_Service.exists_usuario_departamento(db, row["idUsuario"], row["idDepartment"])
                and not row["asignado"]
            ):
                dataExists = {
                    "idUsuario": row["idUsuario"],
                    "idDepartment": row["idDepartment"],
                }
                Usuario_Departamento_Service.deleteUsuario_Departamento_service(db, dataExists)
    
        return {
            "success": True,
            "usuario_departamentos_creados": contador
        }, 201
    except Exception as ex:
        return {
            "success": False,
            "error": str(ex)
        }, 201
    