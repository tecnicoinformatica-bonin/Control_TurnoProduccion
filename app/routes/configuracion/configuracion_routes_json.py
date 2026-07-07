from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.configuracion.configuracion_service import Configuracion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

configuracion_json_bp = Blueprint("configuracion_json_bp", __name__)

@configuracion_json_bp.route("/get_configuraciones", methods=["GET"])
@login_required
@permiso_requerido("configuracion.ver")
def get_configuraciones():
    data = Configuracion_Service.getConfiguraciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@configuracion_json_bp.route("/create_configuracion", methods=["POST"])
@login_required
@permiso_requerido("configuracion.crear")
def create_configuracion():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    result = Configuracion_Service.createConfiguracion_service(db, data)
    return jsonify(result), 201

@configuracion_json_bp.route("/update_configuracion/<int:idConfiguracion>", methods=["PUT"])
@login_required
@permiso_requerido("configuracion.editar")
def update_configuracion(idConfiguracion):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    data["idConfiguracion"] = idConfiguracion
    
    result = Configuracion_Service.updateConfiguracion_service(db, data)
    return jsonify(result), 201

@configuracion_json_bp.route("/delete_configuracion/<int:idConfiguracion>", methods=["DELETE"])
@login_required
@permiso_requerido("configuracion.eliminar")
def delete_configuracion(idConfiguracion):
    result = Configuracion_Service.deleteConfiguracion_service(db, {"idConfiguracion": idConfiguracion})
    if not result:
        return jsonify([]), 400
    return jsonify(result), 201