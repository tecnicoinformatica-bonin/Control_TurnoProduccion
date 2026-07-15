from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.calendario_feriados.calendario_feriados_service import Feriado_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

feriado_json_bp = Blueprint("feriado_json_bp", __name__)

@feriado_json_bp.route("/get_feriados", methods=["GET"])
@login_required
@permiso_requerido("feriado.ver")
def get_feriados():
    data = Feriado_Service.getFeriados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@feriado_json_bp.route("/get_fechas_de_feriados_formateados", methods=["GET"])
@login_required
@permiso_requerido("feriado.ver") 
def get_fechas_de_feriados_formateados():
    data = Feriado_Service.get_fechas_de_feriados_formateados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@feriado_json_bp.route("/get_feriados_formateados", methods=["GET"])
@login_required
@permiso_requerido("feriado.ver")
def get_feriados_formateados():
    data = Feriado_Service.get_feriados_formateados_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@feriado_json_bp.route("/create_feriado", methods=["POST"])
@login_required
@permiso_requerido("feriado.crear")
def create_feriado():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    result = Feriado_Service.createFeriado_service(db, data)
    return jsonify(result), 201

@feriado_json_bp.route("/update_feriado/<int:idFeriado>", methods=["PUT", "POST"])
@login_required
@permiso_requerido("feriado.editar")
def update_feriado(idFeriado):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    data["idFeriado"] = idFeriado

    result = Feriado_Service.updateFeriado_service(db, data)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@feriado_json_bp.route("/delete_feriado/<int:idFeriado>", methods=["DELETE"])
@login_required
@permiso_requerido("feriado.eliminar")
def delete_feriado(idFeriado):
    result = Feriado_Service.deleteFeriado_service(db, {"idFeriado": idFeriado})
    if not result:
        return jsonify([]), 200
    
    return jsonify(result), 200