from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

departamento_json_bp = Blueprint("departamento_json_pb", __name__)

@departamento_json_bp.route('/get_departamentos', methods=["GET"]) 
@login_required
@permiso_requerido("programacion.ver") # De momento solamente se usa en programaciones_general.html
def get_departamentos():
    data = Departamento_Service.getDepartamentos_service(db)
    
    if not data:
        return jsonify([]), 200
    
    return jsonify(data), 200
