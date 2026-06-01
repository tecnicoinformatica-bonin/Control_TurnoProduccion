from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.programacion.programacion_service import Programacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

programacion_json_bp = Blueprint("programacion_json_bp", __name__)

@programacion_json_bp.route("/get_programaciones", methods=["GET"])
@login_required
def get_programaciones():
    data = Programacion_Service.getProgramaciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_counts_by_line/<int:idProgramacion>/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
@permiso_requerido("registro.editar")
def get_counts_by_line(idProgramacion, idDepartment):
    data = Programacion_Service.getCountsByLine_service(db, idProgramacion, idDepartment)
    
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/cerrarProgramacion_json", methods=["PUT"])
@login_required
def cerrarProgramacion_json():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
        
    result = Programacion_Service.cerrarProgramacion_service(db, data)

    if "error" in result:
        return {"error": result['error']}, 400

    return jsonify({"mensaje": result['mensaje']}), 200