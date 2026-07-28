from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

centro_de_costo_json_bp = Blueprint("centro_de_costo_json_bp", __name__)

@centro_de_costo_json_bp.route("/get_centros_de_costo", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver") # De momento se usa solamente en editarProgramacion.html
def get_centros_de_costo():
    data = Centro_de_costo_Service.getCentros_de_costo_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@centro_de_costo_json_bp.route("/get_centros_de_costo_byDepartment_json/<int:idDepartment>", methods=["GET"])
@login_required
@permiso_requerido("centro_de_costo.ver")
def get_centros_de_costo_byDepartmento_json(idDepartment):
    try :
        data = Centro_de_costo_Service.getCentros_de_costoByDepartment_service(db, idDepartment)
        
        if not data:
            return jsonify([]), 200
        
        return jsonify(data), 200
        
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@centro_de_costo_json_bp.route("/isAvailable/<string:nombreCentro_input>/<int:idDepartment>", methods=["POST", "GET"])
@login_required
@permiso_requerido("centro_de_costo.ver")
def exist_centro(nombreCentro_input, idDepartment):
    try :
        data_nombreCentro_input = nombreCentro_input
        data_idDepartment = idDepartment

        data = Centro_de_costo_Service.exist_centro(db, data_nombreCentro_input, data_idDepartment)
        
        if not data:
            return jsonify([]), 200
        
        return jsonify(data), 200
        
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

@centro_de_costo_json_bp.route("/guardar_masivo", methods=["POST"])
@login_required
@permiso_requerido("centro_de_costo.crear")
def guardar_masivo():
    data = request.get_json()

    if not data:
        return {
            "success": False
        }, 400

    for row in data:
        result = Centro_de_costo_Service.exist_centro(db, row["nombreCentro"], row["idDepartment"])

        if not result["available"]:
            continue

        Centro_de_costo_Service.createCentro_de_costo_service(db, row)

    return {
        "success": True,
    }, 201
