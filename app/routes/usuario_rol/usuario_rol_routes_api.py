from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.usuario_rol.usuario_rol_service import Usuario_Rol_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_rol_api_bp = Blueprint("usuario_rol_api_pb", __name__)

@usuario_rol_api_bp.route("/getUsuario_Roles", methods=["GET"])
@login_required
@permiso_requerido("usuario_rol.ver")
def getUsuario_Roles():
    """
    Obtener Usuario_Roles
    ---
    tags:
      - Usuario_Rol
    responses:
      200:
        description: Lista de Usuario_Roles
    """
    usuario_roles = Usuario_Rol_Service.getUsuario_Roles_service(db)

    return jsonify(usuario_roles)

@usuario_rol_api_bp.route("/createUsuario_Rol", methods=["POST"])
@login_required
@permiso_requerido("usuario_rol.crear")
def createUsuario_Rol():
    """
    Crear una nueva Usuario_Rol
    ---
    tags:
      - Usuario_Rol
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
            idRol:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Rol creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_rol = Usuario_Rol_Service.createUsuario_Rol_service(db, data)

    return jsonify(usuario_rol)

@usuario_rol_api_bp.route("/updateUsuario_Rol", methods=["POST"])
@login_required
@permiso_requerido("usuario_rol.editar")
def updateUsuario_Rol():
    """
    Modificar un Usuario_Rol
    ---
    tags:
      - Usuario_Rol
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
            idRol:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Rol modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_rol = Usuario_Rol_Service.updateUsuario_Rol_service(db, data)

    return jsonify(usuario_rol)

@usuario_rol_api_bp.route("/deleteUsuario_Rol", methods=["POST"])
@login_required
@permiso_requerido("usuario_rol.eliminar")
def deleteUsuario_Rol():
    """
    Eliminar un Usuario_Rol
    ---
    tags:
      - Usuario_Rol
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
            idRol:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Rol eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_rol = Usuario_Rol_Service.deleteUsuario_Rol_service(db, data)

    return jsonify(usuario_rol)