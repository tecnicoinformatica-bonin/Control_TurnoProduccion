from flask import Blueprint, jsonify, request
from app.api.rol.rol_service import Rol_Service
from app.extensions.db import db

rol_api_bp = Blueprint("rol_api_pb", __name__)

@rol_api_bp.route("/getRoles", methods=["GET"])
def getRoles():
    """
    Obtener roles
    ---
    tags:
      - Rol
    responses:
      200:
        description: Lista de roles
    """
    roles = Rol_Service.getRols_service(db)

    return jsonify(roles)

@rol_api_bp.route("/createRol", methods=["POST"])
def createRol():
    """
    Crear un nuevo rol
    ---
    tags:
      - Rol
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: nombre
            descripcion:
              type: string
              example: descripcion
    responses:
      200:
        description: Rol creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol = Rol_Service.createRol_service(db, data)

    return jsonify(rol)

@rol_api_bp.route("/updateRol", methods=["POST"])
def updateRol():
    """
    Modificar un rol
    ---
    tags:
      - Rol
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
            nombre:
              type: string
              example: nombre
            descripcion:
              type: string
              example: descripcion
    responses:
      200:
        description: Rol modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol = Rol_Service.updateRol_service(db, data)

    return jsonify(rol)

@rol_api_bp.route("/deleteRol", methods=["POST"])
def deleteRol():
    """
    Eliminar una rol
    ---
    tags:
      - Rol
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
    responses:
      200:
        description: Rol eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol = Rol_Service.deleteRol_service(db, data)

    return jsonify(rol)