from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.calendario_feriados.calendario_feriados_service import Feriado_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

feriado_api_bp = Blueprint("feriado_api_bp", __name__)

@feriado_api_bp.route("/getFeriados", methods=["GET"])
@login_required
@permiso_requerido("feriados.ver")
def getFeriados():
    """
    Obtener feriados
    ---
    tags:
      - Feriado
    responses:
      200:
        description: Lista de feriados
    """
    feriados = Feriado_Service.getFeriados_service(db)

    return jsonify(feriados)

@feriado_api_bp.route("/getFeriadosFormateadas", methods=["GET"])
@login_required
@permiso_requerido("feriados.ver")
def getFeriadosFormateadas():
    """
    Obtener feriados formateados
    ---
    tags:
      - Feriado
    responses:
      200:
        description: Lista de feriados formateados
    """
    feriados = Feriado_Service.get_feriados_formateados_service(db)

    return jsonify(feriados)

@feriado_api_bp.route("/get_fechas_de_feriados_formateados", methods=["GET"])
@login_required
@permiso_requerido("feriados.ver")
def get_fechas_de_feriados_formateados():
    """
    Obtener feriados formateados
    ---
    tags:
      - Feriado
    responses:
      200:
        description: Lista de feriados formateados
    """
    feriados = Feriado_Service.get_fechas_de_feriados_formateados_service(db)

    return jsonify(feriados)

@feriado_api_bp.route("/createFeriado", methods=["POST"])
@login_required
@permiso_requerido("feriados.crear")
def createFeriado():
    """
    Crear un nuevo feriado
    ---
    tags:
      - Feriado
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            fecha:
              type: string
              example: "2026-01-01"
            nombre:
              type: string
              example: "nombre"
            tipo:
              type: string
              example: "asueto"
            es_medio_dia:
              type: boolean
              example: 0
    responses:
      200:
        description: feriado creado correctamente
    """

    # La siguiente feriados es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    feriado = Feriado_Service.createFeriado_service(db, data)

    return jsonify(feriado)

@feriado_api_bp.route("/updateFeriado", methods=["POST"])
@login_required
@permiso_requerido("feriados.editar")
def updateFeriado():
    """
    Modificar un feriado
    ---
    tags:
      - Feriado
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idFeriado:
              type: integer
              example: 1
            fecha:
              type: string
              example: "2026-01-01"
            nombre:
              type: string
              example: "nombre"
            tipo:
              type: string
              example: "asueto"
            es_medio_dia:
              type: boolean
              example: 0
    responses:
      200:
        description: feriado modificada correctamente
    """

    # La siguiente feriados es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    feriado = Feriado_Service.updateFeriado_service(db, data)

    return jsonify(feriado)

@feriado_api_bp.route("/deleteFeriado", methods=["POST"])
@login_required
@permiso_requerido("feriados.eliminar")
def deleteFeriado():
    """
    Eliminar una feriado
    ---
    tags:
      - Feriado
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idFeriado:
              type: integer
              example: 1
    responses:
      200:
        description: feriado eliminada correctamente
    """

    # La siguiente feriados es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    feriado = Feriado_Service.deleteFeriado_service(db, data)

    return jsonify(feriado)