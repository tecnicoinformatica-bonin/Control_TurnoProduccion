from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.registro.registro_service import Registro_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

registro_json_bp = Blueprint("registro_json_pb", __name__)

@registro_json_bp.route("/get_registros/<int:idProgramacion>", methods=["GET"])
@login_required
@permiso_requerido("registro.ver")
def get_registros(idProgramacion):
    data = Registro_Service.getRegistrosByProgramacion_service(db, idProgramacion)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@registro_json_bp.route("/create_registro", methods=["POST"])
@login_required
@permiso_requerido("registro.crear")
def create_registro():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    result = Registro_Service.createRegistro_service(db, data)
    return jsonify(result), 201

@registro_json_bp.route("/update_registro/<int:idRegistro>", methods=["PUT", "POST"])
@login_required
@permiso_requerido("registro.editar")
def update_registro(idRegistro):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    data["idRegistro"] = idRegistro
    result = Registro_Service.updateRegistro_service(db, data)
    return jsonify(result), 200

@registro_json_bp.route("/update_registro_to_nulls/<int:idRegistro>", methods=["PUT", "POST"])
@login_required
@permiso_requerido("registro.editar")
def update_registro_to_nulls(idRegistro):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    data["idRegistro"] = idRegistro
    result = Registro_Service.updateRegistroToNulls_service(db, data)
    return jsonify(result), 200

@registro_json_bp.route("/delete_registro/<int:idRegistro>", methods=["DELETE"])
@login_required
@permiso_requerido("registro.eliminar")
def delete_registro(idRegistro):
    result = Registro_Service.deleteRegistro_service(db, {"idRegistro": idRegistro})
    if not result:
        return jsonify([]), 200
    
    return jsonify(result), 200