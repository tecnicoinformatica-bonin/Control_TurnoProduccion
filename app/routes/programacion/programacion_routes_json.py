from flask import Blueprint, jsonify, request
from app.api.programacion.programacion_service import Programacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

programacion_json_bp = Blueprint("programacion_json_bp", __name__)

@programacion_json_bp.route("/get_programaciones", methods=["GET"])
def get_programaciones():
    data = Programacion_Service.getProgramaciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_counts_by_line/<int:idProgramacion>", methods=["GET"])
@permiso_requerido("programacion.ver")
@permiso_requerido("registro.editar")
def get_counts_by_line(idProgramacion):
    data = Programacion_Service.getCountsByLine_service(db, idProgramacion)
    
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/cerrarProgramacion_json", methods=["PUT"])
def cerrarProgramacion_json():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
        
    result = Programacion_Service.cerrarProgramacion_service(db, data)

    if "error" in result:
        return {"error": result['error']}, 400

    return jsonify({"mensaje": result['mensaje']}), 200