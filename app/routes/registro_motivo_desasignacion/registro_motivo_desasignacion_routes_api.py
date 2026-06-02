from flask import Blueprint, jsonify, request
from app.api.registro_motivo_desasignacion.registro_motivo_desasignacion_service import Registro_motivo_desasignacion_Service
from app.extensions.db import db

registro_motivo_desasignacion_api_bp = Blueprint("registro_motivo_desasignacion_api_bp", __name__)

@registro_motivo_desasignacion_api_bp.route("/get_detalles_motivo_descripcion", methods=["GET"])
def get_detalles_motivo_descripcion():
    """
    Obtener registros_motivo_desasignacion
    ---
    tags:
      - Registro_motivo_desasignacion
    responses:
      200:
        description: Lista de registros_motivo_desasignacion
    """
    registros_motivo_desasignacion = Registro_motivo_desasignacion_Service.get_detalles_motivo_descripcion_service(db)

    return jsonify(registros_motivo_desasignacion)

@registro_motivo_desasignacion_api_bp.route("/getRegistros_motivo_desasignacion_by_idProgramacion/<int:idProgramacion>", methods=["GET"])
def getRegistros_motivo_desasignacion_by_idProgramacion(idProgramacion):
    """
    Obtener registros_motivo_desasignacion
    ---
    tags:
      - Registro_motivo_desasignacion
    responses:
      200:
        description: Lista de registros_motivo_desasignacion
    """
    registros_motivo_desasignacion = Registro_motivo_desasignacion_Service.get_detalles_motivo_descripcion_by_idProgramacion_service(db, idProgramacion)

    return jsonify(registros_motivo_desasignacion)

@registro_motivo_desasignacion_api_bp.route("/createRegistro_motivo_desasignacion", methods=["POST"])
def createRegistro_motivo_desasignacion():
    """
    Crear una nueva registro_motivo_desasignacion
    ---
    tags:
      - Registro_motivo_desasignacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRegistro:
              type: integer
              example: 1
            idMotivo:
              type: integer
              example: 1
    responses:
      200:
        description: registro_motivo_desasignacion creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    registro_motivo_desasignacion = Registro_motivo_desasignacion_Service.createRegistro_registro_motivo_desasignacion_service(db, data)

    return jsonify(registro_motivo_desasignacion)

