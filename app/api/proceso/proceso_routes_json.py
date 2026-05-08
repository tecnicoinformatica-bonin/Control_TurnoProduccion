from flask import Blueprint, jsonify, request
from app.api.proceso.proceso_service import Proceso_Service
from app.extensions.db import db

proceso_json_bp = Blueprint("proceso_json_bp", __name__)

@proceso_json_bp.route("/get_procesos", methods=["GET"])
def get_procesos():
    data = Proceso_Service.getProcesos_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200