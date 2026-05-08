from flask import Blueprint, jsonify, request
from app.api.proceso.proceso_service import Proceso_Service
from app.extensions.db import db

proceso_api_bp = Blueprint("proceso_api_pb", __name__)

@proceso_api_bp.route("/getProcesos", methods=["GET"])
def getProcesos():
    """
    Obtener procesos
    ---
    tags:
      - Proceso
    responses:
      200:
        description: Lista de procesos
    """
    procesos = Proceso_Service.getProcesos_service(db)

    return jsonify(procesos)

@proceso_api_bp.route("/createProceso", methods=["POST"])
def createProceso():
    """
    Crear un nuevo proceso
    ---
    tags:
      - Proceso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            proceso:
              type: string
              example: proceso
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Proceso creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    proceso = Proceso_Service.createProceso_service(db, data)

    return jsonify(proceso)

@proceso_api_bp.route("/updateProceso", methods=["POST"])
def updateProceso():
    """
    Modificar una proceso
    ---
    tags:
      - Proceso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idProceso:
              type: integer
              example: 1
            proceso:
              type: string
              example: proceso
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Proceso modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    proceso = Proceso_Service.updateProceso_service(db, data)

    return jsonify(proceso)

@proceso_api_bp.route("/deleteProceso", methods=["POST"])
def deleteProceso():
    """
    Eliminar una proceso
    ---
    tags:
      - Proceso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idProceso:
              type: integer
              example: 1
    responses:
      200:
        description: Proceso eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    proceso = Proceso_Service.deleteProceso_service(db, data)

    return jsonify(proceso)