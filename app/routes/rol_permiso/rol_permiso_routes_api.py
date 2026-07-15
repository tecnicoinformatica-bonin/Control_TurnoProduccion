from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.rol_permiso.rol_permiso_service import Rol_Permiso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

rol_permiso_api_bp = Blueprint("rol_permiso_api_pb", __name__)

@rol_permiso_api_bp.route("/getRol_Permisos", methods=["GET"])
@login_required
@permiso_requerido("rol_permiso.ver")
def getRol_Permisos():
    """
    Obtener Rol_Permisos
    ---
    tags:
      - Rol_Permiso
    responses:
      200:
        description: Lista de Rol_Permisos
    """
    rol_permisos = Rol_Permiso_Service.getRol_Permisos_service(db)

    return jsonify(rol_permisos)

@rol_permiso_api_bp.route("/createRol_Permiso", methods=["POST"])
@login_required
@permiso_requerido("rol_permiso.crear")
def createRol_Permiso():
    """
    Crear una nueva Rol_Permiso
    ---
    tags:
      - Rol_Permiso
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
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Permiso creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_permiso = Rol_Permiso_Service.createRol_Permiso_service(db, data)

    return jsonify(rol_permiso)

@rol_permiso_api_bp.route("/updateRol_Permiso", methods=["POST"])
@login_required
@permiso_requerido("rol_permiso.editar")
def updateRol_Permiso():
    """
    Modificar un Rol_Permiso
    ---
    tags:
      - Rol_Permiso
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
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Permiso modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_permiso = Rol_Permiso_Service.updateRol_Permiso_service(db, data)

    return jsonify(rol_permiso)

@rol_permiso_api_bp.route("/deleteRol_Permiso", methods=["POST"])
@login_required
@permiso_requerido("rol_permiso.eliminar")
def deleteRol_Permiso():
    """
    Eliminar un Rol_Permiso
    ---
    tags:
      - Rol_Permiso
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
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Rol_Permiso eliminado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    rol_permiso = Rol_Permiso_Service.deleteRol_Permiso_service(db, data)

    return jsonify(rol_permiso)