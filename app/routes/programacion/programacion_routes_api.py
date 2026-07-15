from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.programacion.programacion_service import Programacion_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

programacion_api_bp = Blueprint("programacion_api_pb", __name__)

@programacion_api_bp.route("/getProgramaciones", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
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

@programacion_api_bp.route("/getCountsByLine/<int:idProgramacion>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def getCountsByLine(idProgramacion):
    """
    Comprobar si cumple el mínimo por línea en la programación
    ---
    tags:
      - Programacion
    responses:
      200:
        description: Comprobación de mínimos por línea
    """
    programaciones = Programacion_Service.getCountsByLine_service(db, idProgramacion)

    return jsonify(programaciones)

@programacion_api_bp.route("/getDetallesProgramacionById/<int:idProgramacion>", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
def getDetallesProgramacionById(idProgramacion):
    """
    Obtener programaciones
    ---
    tags:
      - Programacion
    responses:
      200:
        description: Lista de programaciones
    """
    programaciones = Programacion_Service.getDetallesProgramacionByIdProgramacion_service(db, idProgramacion)

    return jsonify(programaciones)

@programacion_api_bp.route("/getProgramacionesEnBorrador", methods=["GET"])
@login_required
@permiso_requerido("programacion.ver")
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
@login_required
@permiso_requerido("programacion.crear")
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
@login_required
@permiso_requerido("programacion.crear")
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
@login_required
@permiso_requerido("programacion.editar")
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
@login_required
@permiso_requerido("programacion.editar")
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
@login_required
@permiso_requerido("programacion.eliminar")
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