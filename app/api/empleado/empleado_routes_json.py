from flask import Blueprint, jsonify, request
from app.api.empleado.empleado_service import Empleado_Service
from app.extensions.db import db

empleado_json_bp = Blueprint("empleado_json_bp", __name__)

@empleado_json_bp.route("/get_empleados", methods=["GET"])
def get_empleados():
    data = Empleado_Service.getEmpleados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200