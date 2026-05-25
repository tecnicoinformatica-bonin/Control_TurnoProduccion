from flask import Blueprint, jsonify, request
from app.api.linea.linea_service import Linea_Service
from app.extensions.db import db

linea_api_bp = Blueprint("linea_api_bp", __name__)

@linea_api_bp.route("/getLineas", methods=["GET"])
def getLineas():
    """
    Obtener lineas
    ---
    tags:
      - Linea
    responses:
      200:
        description: Lista de lineas
    """
    lineas = Linea_Service.getLineas_service(db)

    return jsonify(lineas)

@linea_api_bp.route("/createLinea", methods=["POST"])
def createLinea():
    """
    Crear una nueva linea
    ---
    tags:
      - Linea
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nameLinea:
              type: string
              example: nombreLinea
            idDepartment:
              type: integer
              example: 1
            minimo_requerido:
              type: integer
              example: 10
    responses:
      200:
        description: linea creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    linea = Linea_Service.createLinea_service(db, data)

    return jsonify(linea)

@linea_api_bp.route("/updateLinea", methods=["POST"])
def updateLinea():
    """
    Modificar una linea
    ---
    tags:
      - Linea
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idLinea:
              type: integer
              example: 1
            nameLinea:
              type: string
              example: nombreLinea
            idDepartment:
              type: integer
              example: 1
            minimo_requerido:
              type: integer
              example: 10
    responses:
      200:
        description: linea modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    linea = Linea_Service.updateLinea_service(db, data)

    return jsonify(linea)

@linea_api_bp.route("/deleteLinea", methods=["POST"])
def deleteLinea():
    """
    Eliminar una linea
    ---
    tags:
      - Linea
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idLinea:
              type: integer
              example: 1
    responses:
      200:
        description: linea eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    linea = Linea_Service.deleteLinea_service(db, data)

    return jsonify(linea)