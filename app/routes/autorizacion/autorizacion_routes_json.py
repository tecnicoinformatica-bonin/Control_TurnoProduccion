from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.autorizacion.autorizacion_service import Autorizacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

autorizacion_json_bp = Blueprint("autorizacion_json_bp", __name__)

@autorizacion_json_bp.route("/get_autorizaciones", methods=["GET"])
@login_required
def get_autorizaciones():
    data = Autorizacion_Service.getAutorizaciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@autorizacion_json_bp.route("/get_detalles_autorizaciones/<string:from_date>/<string:to_date>/<int:idDepartment>", methods=["GET"])
@login_required
def get_detalles_autorizaciones(from_date, to_date, idDepartment):
    data = Autorizacion_Service.get_detalles_autorizaciones_service(db, from_date, to_date, idDepartment)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@autorizacion_json_bp.route("/guardar_autorizacion_service", methods=["POST", "PUT"])
@login_required
def guardar_autorizacion_service():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    result = Autorizacion_Service.guardar_autorizacion_service(db, data)
    return jsonify(result), 200