from flask import Blueprint, jsonify, request
from app.api.programacion.programacion_service import Programacion_Service
from app.extensions.db import db

programacion_api_bp = Blueprint("programacion_api_pb", __name__)

@programacion_api_bp.route("/getProgramaciones", methods=["GET"])
def getProgramaciones():
    """
    Obtener programaciones
    ---
    tags:
      - Programacion
    responses:
      200:
        description: Lista de programaciones
    """
    programaciones = Programacion_Service.getProgramaciones_service(db)

    return jsonify(programaciones)

@programacion_api_bp.route("/getProgramacionesEnBorrador", methods=["GET"])
def getProgramacionesEnBorrador():
    """
    Obtener programaciones activos
    ---
    tags:
      - Programacion
    responses:
      200:
        description: Lista de programaciones en borrador
    """
    programaciones = Programacion_Service.getProgramacionesEnBorrador_service(db)

    return jsonify(programaciones)

@programacion_api_bp.route("/createProgramacion", methods=["POST"])
def createProgramacion():
    """
    Crear un nuevo programacion
    ---
    tags:
      - Programacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            fecha:
              type: string
              example: 2026-04-28
            idDepartment:
              type: integer
              example: 5
    responses:
      200:
        description: programacion creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    programacion = Programacion_Service.createProgramacion_service(db, data)

    return jsonify(programacion)

@programacion_api_bp.route("/createProgramacionAutomatica", methods=["POST"])
def createProgramacionAutomatica():
    """
    Crear programaciones de manera automática
    ---
    tags:
      - Programacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            fecha:
              type: string
              example: "2026-04-28"
    responses:
      200:
        description: Programaciones creadas correctamente.
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    programacion = Programacion_Service.createProgramacionAutomatica_service(db, data)

    return jsonify(programacion)

@programacion_api_bp.route("/cerrarProgramacion", methods=["POST"])
def cerrarProgramacion():
    """
    Cerrar una programación.
    ---
    tags:
      - Programacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            fecha_cierre:
              type: string
              example: "2026-04-04"
            idProgramacion:
              type: integer
              example: 1
            elaborado_por:
              type: int
              example: 9
            cerrado_por:
              type: int
              example: 1
            estado:
              type: string
              example: "CERRADO"
    responses:
      200:
        description: Programacion cerrada correctamente.
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    programacion = Programacion_Service.cerrarProgramacion_service(db, data)

    return jsonify(programacion)

@programacion_api_bp.route("/reOpenProgramacion", methods=["POST"])
def reOpenProgramacion():
    """
    Reabrir una programación.
    ---
    tags:
      - Programacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            fecha:
              type: string
              example: 2026-04-28
            idDepartment:
              type: integer
              example: 5
            reabierto_por:
              type: string
              example: user
            motivo_reapertura:
              type: string
              example: user_c
    responses:
      200:
        description: Programación reabierta correctamente.
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    programacion = Programacion_Service.reOpenProgramacion_service(db, data)

    return jsonify(programacion)

@programacion_api_bp.route("/deleteProgramacion", methods=["POST"])
def deleteProgramacion():
    """
    Eliminar una programación.
    ---
    tags:
      - Programacion
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idProgramacion:
              type: integer
              example: 5
    responses:
      200:
        description: Programación deliminada correctamente.
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    programacion = Programacion_Service.deleteProgramacion_service(db, data)

    return jsonify(programacion)