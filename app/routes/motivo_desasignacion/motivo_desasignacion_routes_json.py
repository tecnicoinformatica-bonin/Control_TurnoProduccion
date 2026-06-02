from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.motivo_desasignacion.motivo_desasignacion_service import Motivo_desasignacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

motivo_desasignacion_json_bp = Blueprint("motivo_desasignacion_json_bp", __name__)

@motivo_desasignacion_json_bp.route("/get_motivos_desasignacion", methods=["GET"])
@login_required
def get_motivos_desasignacion():
    data = Motivo_desasignacion_Service.getMotivos_desasignacion_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200