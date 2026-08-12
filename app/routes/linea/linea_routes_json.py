from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.linea.linea_service import Linea_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

linea_json_bp = Blueprint("linea_json_bp", __name__)

@linea_json_bp.route("/get_lineas", methods=["GET"])
@login_required
@permiso_requerido("linea.ver")
def get_lineas():
    data = Linea_Service.getLineas_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@linea_json_bp.route("/get_lineas_details", methods=["GET"])
@login_required
@permiso_requerido("linea.ver")
def get_lineas_details():
    data = Linea_Service.get_lineas_details_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@linea_json_bp.route("/get_lineas_by_department/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "linea.ver")
def getLineasByDepartment(idDepartment):
    data = Linea_Service.getLineasByDepartment_service(db, idDepartment)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@linea_json_bp.route("/guardar_masivo", methods=["POST"])
@login_required
@permiso_requerido("linea.crear")
def guardar_masivo():
    data = request.get_json()

    if not data:
        return {
            "success": False
        }, 400

    for row in data:
        result = Linea_Service.exist_linea(db, row["nameLinea"], row["idDepartment"])
        
        if not result["available"]:
            continue

        Linea_Service.createLinea_service(db, row)

    return {
        "success": True,
    }, 201