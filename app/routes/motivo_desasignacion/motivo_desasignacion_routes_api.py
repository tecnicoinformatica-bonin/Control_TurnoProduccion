from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.motivo_desasignacion.motivo_desasignacion_service import Motivo_desasignacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

motivo_desasignacion_api_bp = Blueprint("motivo_desasignacion_api_bp", __name__)

@motivo_desasignacion_api_bp.route("/getMotivos_desasignacion", methods=["GET"])
@login_required
@permiso_requerido("motivo_desasignacion.ver")
def getMotivos_desasignacion():
    """
    Obtener motivos_desasignacion
    ---
    tags:
      - Motivo_desasignacion
    responses:
      200:
        description: Lista de motivos_desasignacion
    """
    motivos_desasignacion = Motivo_desasignacion_Service.getMotivos_desasignacion_service(db)

    return jsonify(motivos_desasignacion)

@motivo_desasignacion_api_bp.route("/createMotivo_desasignacion", methods=["POST"])
@login_required
@permiso_requerido("motivo_desasignacion.crear")
def createMotivo_desasignacion():
    """
    Crear una nueva motivo_desasignacion
    ---
    tags:
      - Motivo_desasignacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcion:
              type: string
              example: descripcion
    responses:
      200:
        description: motivo_desasignacion creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    motivo_desasignacion = Motivo_desasignacion_Service.createMotivo_desasignacion_service(db, data)

    return jsonify(motivo_desasignacion)

@motivo_desasignacion_api_bp.route("/updateMotivo_desasignacion", methods=["POST"])
@login_required
@permiso_requerido("motivo_desasignacion.editar")
def updateMotivo_desasignacion():
    """
    Modificar una motivo_desasignacion
    ---
    tags:
      - Motivo_desasignacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idMotivo:
              type: integer
              example: 1
            descripcion:
              type: string
              example: descripcion
            
    responses:
      200:
        description: motivo_desasignacion modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    motivo_desasignacion = Motivo_desasignacion_Service.updateMotivo_desasignacion_service(db, data)

    return jsonify(motivo_desasignacion)

@motivo_desasignacion_api_bp.route("/deleteMotivo_desasignacion", methods=["POST"])
@login_required
@permiso_requerido("motivo_desasignacion.eliminar")
def deleteMotivo_desasignacion():
    """
    Eliminar una motivo_desasignacion
    ---
    tags:
      - Motivo_desasignacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idMotivo:
              type: integer
              example: 1
    responses:
      200:
        description: motivo_desasignacion eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    motivo_desasignacion = Motivo_desasignacion_Service.deleteMotivo_desasignacion_service(db, data)

    return jsonify(motivo_desasignacion)