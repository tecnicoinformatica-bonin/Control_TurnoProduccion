from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import login_required
from app.api.usuario.usuario_service import Usuario_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_api_bp = Blueprint("usuario_api_bp", __name__)

@usuario_api_bp.route("/getUsuarios", methods=["GET"])
@login_required
@permiso_requerido("usuario.ver")
def getUsuarios():
    """
    Obtener usuarios
    ---
    tags:
      - Usuario
    responses:
        200:
            description: Lista de Usuarios
    """
    usuarios = Usuario_Service.getUsuarios_service(db)

    return jsonify(usuarios)

@usuario_api_bp.route("/createUsuario", methods=["POST"])
@login_required
@permiso_requerido("usuario.crear")
def createUsuario():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Usuario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            nombre:
              type: string
              example: Administrador
            password:
              type: string
              example: Admin123
            activo:
              type: boolean
              example: 1
    responses:
      200:
        description: Usuario creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    usuario = Usuario_Service.createUsuario_service(db, data)

    return jsonify(usuario)

@usuario_api_bp.route("/login", methods=["POST"])
def login():
    """
    Login de usuario
    ---
    tags:
      - Usuario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: Admin123
    responses:
      200:
        description: Login exitoso
    """

    data = request.get_json(silent=True)

    resultado = Usuario_Service.login_service(db, data)

    return jsonify(resultado)

#@usuario_api_bp.route("/getUsuarioAndRol", methods=["POST"])
#def getUsuarioAndRol():
    """
    Obtener usuario con rol asignado
    ---
    tags:
      - Usuario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              format: int64
              example: 1
    responses:
      200:
        description: Usuario obtenido correctamente
    """

    #data = request.get_json()

    #result = Usuario_Service.getUsuarioRol_service(db, data)

    #return jsonify(result)