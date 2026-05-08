from flask import Blueprint, jsonify, request
from app.api.linea.linea_service import Linea_Service
from app.extensions.db import db

linea_json_bp = Blueprint("linea_json_bp", __name__)

@linea_json_bp.route("/get_lineas", methods=["GET"])
def get_lineas():
    data = Linea_Service.getLineas_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200