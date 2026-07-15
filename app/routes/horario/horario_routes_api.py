from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.horario.horario_service import Horario_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

horario_api_bp = Blueprint("horario_api_bp", __name__)

@horario_api_bp.route("/getHorarios", methods=["GET"])
@login_required
@permiso_requerido("horario.ver")
def getHorarios():
    """
    Obtener horarios
    ---
    tags:
      - Horario
    responses:
      200:
        description: Lista de horarios
    """
    horarios = Horario_Service.getHorarios_service(db)

    return jsonify(horarios)

@horario_api_bp.route("/createHorario", methods=["POST"])
@login_required
@permiso_requerido("horario.crear")
def createHorario():
    """
    Crear una nueva horario
    ---
    tags:
      - Horario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descripcionHorario:
              type: string
              example: "descripcionHorario"
            hora_inicio:
              type: string
              example: "07:00:00"
            hora_fin:
              type: string
              example: "16:00:00"
    responses:
      200:
        description: horario creada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    horario = Horario_Service.createHorario_service(db, data)

    return jsonify(horario)

@horario_api_bp.route("/updateHorario", methods=["POST"])
@login_required
@permiso_requerido("horario.editar")
def updateHorario():
    """
    Modificar una horario
    ---
    tags:
      - Horario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idHoario:
              type: integer
              example: 1
            descripcionHorario:
              type: string
              example: "descripcionHorario"
            hora_inicio:
              type: string
              example: "07:00:00"
            hora_fin:
              type: string
              example: "16:00:00"            
    responses:
      200:
        description: horario modificada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    horario = Horario_Service.updateHorario_service(db, data)

    return jsonify(horario)

@horario_api_bp.route("/deleteHorario", methods=["POST"])
@login_required
@permiso_requerido("horario.eliminar")
def deleteHorario():
    """
    Eliminar una horario
    ---
    tags:
      - Horario
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idHoario:
              type: integer
              example: 1
    responses:
      200:
        description: horario eliminada correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    horario = Horario_Service.deleteHorario_service(db, data)

    return jsonify(horario)