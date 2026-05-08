from flask import Blueprint, jsonify, request
from app.api.programacion.programacion_service import Programacion_Service
from app.extensions.db import db

programacion_json_bp = Blueprint("programacion_json_bp", __name__)

@programacion_json_bp.route("/get_programaciones", methods=["GET"])
def get_programaciones():
    data = Programacion_Service.getProgramacions_service(db)
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