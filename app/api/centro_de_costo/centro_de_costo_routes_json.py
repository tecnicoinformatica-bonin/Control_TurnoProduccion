from flask import Blueprint, jsonify, request
from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.extensions.db import db

centro_de_costo_json_bp = Blueprint("centro_de_costo_json_bp", __name__)

@centro_de_costo_json_bp.route("/get_centros_de_costo", methods=["GET"])
def get_centros_de_costo():
    data = Centro_de_costo_Service.getCentros_de_costo_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@centro_de_costo_json_bp.route("/get_centros_de_costo_byDepartment_json/<int:idDepartment>", methods=["GET"])
def get_centros_de_costo_byDepartmento_json(idDepartment):
    try :
        data = Centro_de_costo_Service.getCentros_de_costoByDepartment_service(db, idDepartment)
        
        if not data:
            return jsonify([]), 200
        
        return jsonify(data), 200
        
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
