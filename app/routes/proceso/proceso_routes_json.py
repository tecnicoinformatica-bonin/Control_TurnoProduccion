from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.proceso.proceso_service import Proceso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

proceso_json_bp = Blueprint("proceso_json_bp", __name__)

@proceso_json_bp.route("/get_procesos", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "proceso.ver")
def get_procesos():
    data = Proceso_Service.getProcesos_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@proceso_json_bp.route("/get_procesos_by_department/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "proceso.ver")
def get_procesos_by_department(idDepartment):
    data = Proceso_Service.getProcesosByDepartment_service(db, idDepartment)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200