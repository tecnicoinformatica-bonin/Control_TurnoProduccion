from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.registro_motivo_desasignacion.registro_motivo_desasignacion_service import Registro_motivo_desasignacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

registro_motivo_desasignacion_json_bp = Blueprint("registro_motivo_desasignacion_json_bp", __name__)

@registro_motivo_desasignacion_json_bp.route("/get_count_motivos_desasignacion/<string:from_date>/<string:to_date>", methods=["GET"])
@login_required
@permiso_requerido("registro_motivo_desasignacion.ver")
def get_count_motivos_desasignacion(from_date, to_date):
    data = Registro_motivo_desasignacion_Service.get_count_motivos_desasignacion_service(db, from_date, to_date)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@registro_motivo_desasignacion_json_bp.route("/get_registros_motivo_desasignacion", methods=["GET"])
@login_required
@permiso_requerido("registro_motivo_desasignacion.ver")
def get_registros_motivo_desasignacion():
    data = Registro_motivo_desasignacion_Service.get_detalles_motivo_descripcion_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@registro_motivo_desasignacion_json_bp.route("/get_registros_motivo_desasignacion_by_idProgramacion/<int:idProgramacion>", methods=["GET"])
@login_required
@permiso_requerido("registro_motivo_desasignacion.ver")
def get_registros_motivo_desasignacion_by_idProgramacion(idProgramacion):
    data = Registro_motivo_desasignacion_Service.get_detalles_motivo_descripcion_by_idProgramacion_service(db, idProgramacion)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@registro_motivo_desasignacion_json_bp.route("/createRegistro_registro_motivo_desasignacion", methods=["POST"])
@login_required
@permiso_requerido("registro_motivo_desasignacion.crear")
def createRegistro_registro_motivo_desasignacion():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    result = Registro_motivo_desasignacion_Service.createRegistro_registro_motivo_desasignacion_service(db, data)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 201