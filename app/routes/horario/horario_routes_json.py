from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.horario.horario_service import Horario_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

horario_json_bp = Blueprint("horario_json_bp", __name__)

@horario_json_bp.route("/get_horarios", methods=["GET"])
@login_required
@permiso_requerido("horario.ver")
def get_horarios():
    data = Horario_Service.getHorarios_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200