from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.rol.rol_service import Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

rol_json_bp = Blueprint("rol_json_bp", __name__)

@rol_json_bp.route("/get_roles_details", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "rol.ver")
def get_roles():
    data = Rol_Service.getRoles_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200


