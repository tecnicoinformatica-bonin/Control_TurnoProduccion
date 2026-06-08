from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.marcaje.marcaje_service import Marcaje_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

marcaje_json_bp = Blueprint("marcaje_json_bp", __name__)

@marcaje_json_bp.route("/get_summary_of_clocks/<string:fecha>", methods=["GET"])
@login_required
def get_marcajes(fecha):
    data = Marcaje_Service.get_summary_of_clocks_service(fecha)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

