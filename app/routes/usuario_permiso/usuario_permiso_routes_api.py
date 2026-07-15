from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.usuario_permiso.usuario_permiso_service import Usuario_Permiso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_permiso_api_bp = Blueprint("usuario_permiso_api_pb", __name__)

@usuario_permiso_api_bp.route("/getUsuario_Permisos", methods=["GET"])
@login_required
@permiso_requerido("usuario_permiso.ver")
def getUsuario_Permisos():
    """
    Obtener Usuario_Permisos
    ---
    tags:
      - Usuario_Permiso
    responses:
      200:
        description: Lista de Usuario_Permisos
    """
    usuario_permisos = Usuario_Permiso_Service.getUsuario_Permisos_service(db)

    return jsonify(usuario_permisos)

@usuario_permiso_api_bp.route("/createUsuario_Permiso", methods=["POST"])
@login_required
@permiso_requerido("usuario_permiso.crear")
def createUsuario_Permiso():
    """
    Crear una nueva Usuario_Permiso
    ---
    tags:
      - Usuario_Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idUsuario:
              type: integer
              example: 1
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Permiso creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_permiso = Usuario_Permiso_Service.createUsuario_Permiso_service(db, data)

    return jsonify(usuario_permiso)

@usuario_permiso_api_bp.route("/updateUsuario_Permiso", methods=["POST"])
@login_required
@permiso_requerido("usuario_permiso.editar")
def updateUsuario_Permiso():
    """
    Modificar un Usuario_Permiso
    ---
    tags:
      - Usuario_Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idUsuario:
              type: integer
              example: 1
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Permiso modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_permiso = Usuario_Permiso_Service.updateUsuario_Permiso_service(db, data)

    return jsonify(usuario_permiso)

@usuario_permiso_api_bp.route("/deleteUsuario_Permiso", methods=["POST"])
@login_required
@permiso_requerido("usuario_permiso.eliminar")
def deleteUsuario_Permiso():
    """
    Eliminar un Usuario_Permiso
    ---
    tags:
      - Usuario_Permiso
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idUsuario:
              type: integer
              example: 1
            idPermiso:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Permiso eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_permiso = Usuario_Permiso_Service.deleteUsuario_Permiso_service(db, data)

    return jsonify(usuario_permiso)