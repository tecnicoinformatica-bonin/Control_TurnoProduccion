from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.api.programacion.programacion_service import Programacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

programacion_json_bp = Blueprint("programacion_json_bp", __name__)

@programacion_json_bp.route("/get_programaciones", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_programaciones():
    data = Programacion_Service.getProgramaciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_programaciones_activas", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_programaciones_activas():
    data = Programacion_Service.getProgramacionesActivas_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_programaciones_activas_by_idDepartment", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_programaciones_activas_by_idDepartment():
    data = Programacion_Service.getProgramacionesActivasByIdDepartments_service(db, current_user.id)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_programaciones_cerradas", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_programaciones_cerradas():
    data = Programacion_Service.getProgramacionesCerradas_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_programaciones_cerradas_by_idDepartment", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_programaciones_cerradas_by_idDepartment():
    data = Programacion_Service.getProgramacionesCerradasByIdDepartments_service(db, current_user.id)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_filtros_programacion/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def get_filtros_programacion(idDepartment):
    data = Programacion_Service.get_filtros_programacion_service(db, idDepartment)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/get_counts_by_line/<int:idProgramacion>/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver", "registro.editar")
def get_counts_by_line(idProgramacion, idDepartment):
    data = Programacion_Service.getCountsByLine_service(db, idProgramacion, idDepartment)
    
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@programacion_json_bp.route("/cerrarProgramacion_json", methods=["PUT"])
@login_required
@permiso_requerido("programacion.editar")
def cerrarProgramacion_json():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
        
    result = Programacion_Service.cerrarProgramacion_service(db, data)

    if "error" in result:
        return {"error": result['error']}, 400

    return jsonify({"mensaje": result['mensaje']}), 200