from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

centro_de_costo_api_bp = Blueprint("centro_de_costo_api_pb", __name__)

@centro_de_costo_api_bp.route("/getCentros_de_costo", methods=["GET"])
@login_required
@permiso_requerido("centro_de_costo.ver")
def getCentros_de_costo():
    """
    Obtener centros_de_costo
    ---
    tags:
      - Centro_de_costo
    responses:
      200:
        description: Lista de centros_de_costo
    """
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)

    return jsonify(centros_de_costo)

@centro_de_costo_api_bp.route("/createCentro_de_costo", methods=["POST"])
@login_required
@permiso_requerido("centro_de_costo.crear")
def createCentro_de_costo():
    """
    Crear un nuevo centro_de_costo
    ---
    tags:
      - Centro_de_costo
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombreCentro:
              type: string
              example: "nombreCentro"
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: centro_de_costo creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    centro_de_costo = Centro_de_costo_Service.createCentro_de_costo_service(db, data)

    return jsonify(centro_de_costo)

@centro_de_costo_api_bp.route("/updateCentro_de_costo", methods=["POST"])
@login_required
@permiso_requerido("centro_de_costo.editar")
def updateCentro_de_costo():
    """
    Modificar un centro_de_costo
    ---
    tags:
      - Centro_de_costo
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idCentro:
              type: integer
              example: 1
            nombreCentro:
              type: string
              example: "nombreCentro"
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: centro_de_costo modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    centro_de_costo = Centro_de_costo_Service.updateCentro_de_costo_service(db, data)

    return jsonify(centro_de_costo)

@centro_de_costo_api_bp.route("/deleteCentro_de_costo", methods=["POST"])
@login_required
@permiso_requerido("centro_de_costo.eliminar")
def deleteCentro_de_costo():
    """
    Eliminar un centro_de_costo
    ---
    tags:
      - Centro_de_costo
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idCentro:
              type: integer
              example: 1
    responses:
      200:
        description: centro_de_costo eliminado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    centro_de_costo = Centro_de_costo_Service.deleteCentro_de_costo_service(db, data)

    return jsonify(centro_de_costo)