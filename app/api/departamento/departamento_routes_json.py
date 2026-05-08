from flask import Blueprint, jsonify, request
from app.api.registro.registro_service import Registro_Service
from app.extensions.db import db

registro_json_bp = Blueprint("registro_json_pb", __name__)

@registro_json_bp.route("/get_registros/<int:idProgramacion>", methods=["GET"])
def get_registros(idProgramacion):
    data = Registro_Service.getRegistrosByProgramacion_service(db, idProgramacion)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@registro_json_bp.route("/create_registro", methods=["POST"])
def create_registro():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    result = Registro_Service.createRegistro_service(db, data)
    return jsonify(result), 201

@registro_json_bp.route("/update_registro/<int:idRegistro>", methods=["PUT"])
def update_registro(idRegistro):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    data["idRegistro"] = idRegistro
    result = Registro_Service.updateRegistro_service(db, data)
    return jsonify(result), 200

@registro_json_bp.route("/delete_registro/<int:idRegistro>", methods=["DELETE"])
def delete_registro(idRegistro):
    result = Registro_Service.deleteRegistro_service(db, {"idRegistro": idRegistro})
    if not result:
        return jsonify([]), 200
    
    return jsonify(result), 200