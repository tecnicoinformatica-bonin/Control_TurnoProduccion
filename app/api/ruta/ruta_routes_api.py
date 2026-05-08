from flask import Blueprint, jsonify, request
from app.api.ruta.ruta_service import Ruta_Service
from app.extensions.db import db

ruta_api_bp = Blueprint("ruta_api_pb", __name__)

@ruta_api_bp.route("/getRutas", methods=["GET"])
def getRutas():
    """
    Obtener rutas
    ---
    tags:
      - Ruta
    responses:
      200:
        description: Lista de rutas
    """
    rutas = Ruta_Service.getRutas_service(db)

    return jsonify(rutas)

@ruta_api_bp.route("/createRuta", methods=["POST"])
def createRuta():
    """
    Crear una nueva ruta
    ---
    tags:
      - Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            path:
              type: string
              example: path
    responses:
      200:
        description: Ruta creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    ruta = Ruta_Service.createRuta_service(db, data)

    return jsonify(ruta)

@ruta_api_bp.route("/updateRuta", methods=["POST"])
def updateRuta():
    """
    Modificar una ruta
    ---
    tags:
      - Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRuta:
              type: integer
              example: 1
            path:
              type: string
              example: path
    responses:
      200:
        description: Ruta modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    ruta = Ruta_Service.updateRuta_service(db, data)

    return jsonify(ruta)

@ruta_api_bp.route("/deleteRuta", methods=["POST"])
def deleteRuta():
    """
    Eliminar una ruta
    ---
    tags:
      - Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRuta:
              type: integer
              example: 1
    responses:
      200:
        description: Ruta eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    ruta = Ruta_Service.deleteRuta_service(db, data)

    return jsonify(ruta)