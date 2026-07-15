from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.permiso.permiso_service import Permiso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

permiso_api_bp = Blueprint("permiso_api_bp", __name__)

@permiso_api_bp.route("/getPermisos", methods=["GET"])
@login_required
@permiso_requerido("permiso.ver")
def getPermisos():
    """
    Obtener permisos
    ---
    tags:
      - Permiso
    responses:
      200:
        description: Lista de permisos
    """
    permisos = Permiso_Service.getPermisos_service(db)

    return jsonify(permisos)

@permiso_api_bp.route("/createPermiso", methods=["POST"])
@login_required
@permiso_requerido("permiso.crear")
def createPermiso():
    """
    Crear una nueva permiso
    ---
    tags:
      - Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombrePermiso:
              type: string
              example: "nombrePermiso"
            descripcion:
              type: string
              example: "descripcion"
    responses:
      200:
        description: permiso creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    permiso = Permiso_Service.createPermiso_service(db, data)

    return jsonify(permiso)

@permiso_api_bp.route("/updatePermiso", methods=["POST"])
@login_required
@permiso_requerido("permiso.editar")
def updatePermiso():
    """
    Modificar una permiso
    ---
    tags:
      - Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idPermiso:
              type: integer
              example: 1
            nombrePermiso:
              type: string
              example: "nombrePermiso"
            descripcion:
              type: string
              example: "descripcion"
    responses:
      200:
        description: permiso modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    permiso = Permiso_Service.updatePermiso_service(db, data)

    return jsonify(permiso)

@permiso_api_bp.route("/deletePermiso", methods=["POST"])
@login_required
@permiso_requerido("permiso.eliminar")
def deletePermiso():
    """
    Eliminar una permiso
    ---
    tags:
      - Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: permiso eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    permiso = Permiso_Service.deletePermiso_service(db, data)

    return jsonify(permiso)