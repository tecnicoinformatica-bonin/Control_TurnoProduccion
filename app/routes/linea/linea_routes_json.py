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

@linea_json_bp.route("/get_lineas_by_department/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "linea.ver")
def getLineasByDepartment(idDepartment):
    data = Linea_Service.getLineasByDepartment_service(db, idDepartment)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200