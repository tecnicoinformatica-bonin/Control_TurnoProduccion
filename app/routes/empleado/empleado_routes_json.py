from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.empleado.empleado_service import Empleado_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

empleado_json_bp = Blueprint("empleado_json_bp", __name__)

@empleado_json_bp.route("/get_empleados", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver") # Solo uso en editarProgramacion.html
def get_empleados():
    data = Empleado_Service.getEmpleados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@empleado_json_bp.route("/get_full_name_empleados", methods=["GET"])
@login_required
@permiso_requerido("empleado.ver")
def get_full_name_empleados():
    data = Empleado_Service.get_full_name_empleados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200