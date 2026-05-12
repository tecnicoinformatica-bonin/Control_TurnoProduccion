from flask import Blueprint, jsonify, request
from app.api.permiso.permiso_service import Permiso_Service
from app.extensions.db import db

permiso_json_bp = Blueprint("permiso_json_bp", __name__)

@permiso_json_bp.route("/get_permisos", methods=["GET"])
def get_permisos():
    data = Permiso_Service.getPermisos_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200