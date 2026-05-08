from flask import Blueprint, jsonify, request
from app.api.rol_ruta.rol_ruta_service import Rol_Ruta_Service
from app.extensions.db import db

rol_ruta_api_bp = Blueprint("rol_ruta_api_pb", __name__)

@rol_ruta_api_bp.route("/getRol_Rutas", methods=["GET"])
def getRol_Rutas():
    """
    Obtener Rol_Rutas
    ---
    tags:
      - Rol_Ruta
    responses:
      200:
        description: Lista de Rol_Rutas
    """
    rol_rutas = Rol_Ruta_Service.getRol_Rutas_service(db)

    return jsonify(rol_rutas)

@rol_ruta_api_bp.route("/createRol_Ruta", methods=["POST"])
def createRol_Ruta():
    """
    Crear una nueva Rol_Ruta
    ---
    tags:
      - Rol_Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRol:
              type: integer
              example: 1
            idRuta:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Ruta creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_ruta = Rol_Ruta_Service.createRol_Ruta_service(db, data)

    return jsonify(rol_ruta)

@rol_ruta_api_bp.route("/updateRol_Ruta", methods=["POST"])
def updateRol_Ruta():
    """
    Modificar un Rol_Ruta
    ---
    tags:
      - Rol_Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRol:
              type: integer
              example: 1
            idRuta:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Ruta modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_ruta = Rol_Ruta_Service.updateRol_Ruta_service(db, data)

    return jsonify(rol_ruta)

@rol_ruta_api_bp.route("/deleteRol_Ruta", methods=["POST"])
def deleteRol_Ruta():
    """
    Eliminar un Rol_Ruta
    ---
    tags:
      - Rol_Ruta
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRol:
              type: integer
              example: 1
            idRuta:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Ruta eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_ruta = Rol_Ruta_Service.deleteRol_Ruta_service(db, data)

    return jsonify(rol_ruta)