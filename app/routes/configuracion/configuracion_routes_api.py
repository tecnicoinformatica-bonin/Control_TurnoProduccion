from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.configuracion.configuracion_service import Configuracion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

configuracion_api_bp = Blueprint("configuracion_api_bp", __name__)

@configuracion_api_bp.route("/getConfiguraciones", methods=["GET"])
@login_required
@permiso_requerido("configuracion.ver")
def getConfiguraciones():
    """
    Obtener configuraciones
    ---
    tags:
      - Configuracion
    responses:
      200:
        description: Lista de configuraciones
    """
    configuraciones = Configuracion_Service.getConfiguraciones_service(db)

    return jsonify(configuraciones)

@configuracion_api_bp.route("/createConfiguracion", methods=["POST"])
@login_required
@permiso_requerido("configuracion.crear")
def createConfiguracion():
    """
    Crear un nuevo configuracion
    ---
    tags:
      - Configuracion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            categoria:
              type: string
              example: "categoria"
            clave:
              type: string
              example: "clave"
            valor:
              type: string
              example: "valor"
            tipo:
              type: string
              example: "tipo"
            descripcion:
              type: string
              example: "descripcion"
    responses:
      200:
        description: Configuracion creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    configuracion = Configuracion_Service.createConfiguracion_service(db, data)

    return jsonify(configuracion)

@configuracion_api_bp.route("/updateConfiguracion", methods=["POST"])
@login_required
@permiso_requerido("configuracion.editar")
def updateConfiguracion():
    """
    Modificar una configuracion
    ---
    tags:
      - Configuracion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idConfiguracion:
              type: integer
              example: 1
            categoria:
              type: string
              example: "categoria"
            clave:
              type: string
              example: "clave"
            valor:
              type: string
              example: "valor"
            tipo:
              type: string
              example: "tipo"
            descripcion:
              type: string
              example: "descripcion"
    responses:
      200:
        description: Configuracion modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    configuracion = Configuracion_Service.updateConfiguracion_service(db, data)

    return jsonify(configuracion)

@configuracion_api_bp.route("/deleteConfiguracion", methods=["POST"])
@login_required
@permiso_requerido("configuracion.eliminar")
def deleteConfiguracion():
    """
    Eliminar una configuracion
    ---
    tags:
      - Configuracion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idConfiguracion:
              type: integer
              example: 1
    responses:
      200:
        description: Configuracion eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    configuracion = Configuracion_Service.deleteConfiguracion_service(db, data)

    return jsonify(configuracion)