from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.permiso.permiso_service import Permiso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

permiso_json_bp = Blueprint("permiso_json_bp", __name__)

@permiso_json_bp.route("/get_permisos", methods=["GET"])
@login_required
@permiso_requerido("permiso.ver")
def get_permisos():
    data = Permiso_Service.getPermisos_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@permiso_json_bp.route("/get_permisos_asignados_por_rol/<int:idRol>", methods=["GET"])
@login_required
@permiso_requerido("permiso.ver")
def get_permisos_asignados_por_rol(idRol):
    data = Permiso_Service.get_permisos_asignados_por_rol_service(db, idRol)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@permiso_json_bp.route("/get_permisos_asignados_por_usuario/<int:idUsuario>", methods=["GET"])
@login_required
@permiso_requerido("permiso.ver")
def get_permisos_asignados_por_usuario(idUsuario):
    data = Permiso_Service.get_permisos_asignados_por_usuario_service(db, idUsuario)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200