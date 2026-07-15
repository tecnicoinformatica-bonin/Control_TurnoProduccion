from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.usuario_departamento.usuario_departamento_service import Usuario_Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_departamento_api_bp = Blueprint("usuario_departamento_api_pb", __name__)

@usuario_departamento_api_bp.route("/getUsuario_Departamentos", methods=["GET"])
@login_required
@permiso_requerido("usuario_departamento.ver")
def getUsuario_Departamentos():
    """
    Obtener Usuario_Departamentos
    ---
    tags:
      - Usuario_Departamento
    responses:
      200:
        description: Lista de Usuario_Departamentos
    """
    usuario_departamentos = Usuario_Departamento_Service.getUsuario_Departamentos_service(db)

    return jsonify(usuario_departamentos)

@usuario_departamento_api_bp.route("/createUsuario_Departamento", methods=["POST"])
@login_required
@permiso_requerido("usuario_departamento.crear")
def createUsuario_Departamento():
    """
    Crear una nueva Usuario_Departamento
    ---
    tags:
      - Usuario_Departamento
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
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Departamento creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_departamento = Usuario_Departamento_Service.createUsuario_Departamento_service(db, data)

    return jsonify(usuario_departamento)

@usuario_departamento_api_bp.route("/updateUsuario_Departamento", methods=["POST"])
@login_required
@permiso_requerido("usuario_departamento.editar")
def updateUsuario_Departamento():
    """
    Modificar un Usuario_Departamento
    ---
    tags:
      - Usuario_Departamento
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
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Departamento modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_departamento = Usuario_Departamento_Service.updateUsuario_Departamento_service(db, data)

    return jsonify(usuario_departamento)

@usuario_departamento_api_bp.route("/deleteUsuario_Departamento", methods=["POST"])
@login_required
@permiso_requerido("usuario_departamento.eliminar")
def deleteUsuario_Departamento():
    """
    Eliminar un Usuario_Departamento
    ---
    tags:
      - Usuario_Departamento
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
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Usuario_Departamento eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario_departamento = Usuario_Departamento_Service.deleteUsuario_Departamento_service(db, data)

    return jsonify(usuario_departamento)