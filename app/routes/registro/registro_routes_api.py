from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.registro.registro_service import Registro_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

registro_api_bp = Blueprint("registro_api_pb", __name__)

@registro_api_bp.route("/getRegistros", methods=["GET"])
@login_required
@permiso_requerido("registro.ver")
def getRegistros():
    """
    Obtener registros
    ---
    tags:
      - Registro
    responses:
      200:
        description: Lista de registros
    """
    registros = Registro_Service.getRegistros_service(db)

    return jsonify(registros)

@registro_api_bp.route("/getDetalleRegistrosByProgramacion/<int:idProgramacion>", methods=["GET"])
@login_required
@permiso_requerido("registro.ver")
def getDetalleRegistrosByProgramacion(idProgramacion):
    """
    Obtener registros
    ---
    tags:
      - Registro
    responses:
      200:
        description: Lista de registros
    """
    registros = Registro_Service.getDetalleRegistrosByProgramacion_service(db, idProgramacion)

    return jsonify(registros)

@registro_api_bp.route("/createRegistro", methods=["POST"])
@login_required
@permiso_requerido("registro.crear")
def createRegistro():
    """
    Crear un nuevo registro
    ---
    tags:
      - Registro
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idProgramacion:
              type: integer
              example: 1
            idEmpleado:
              type: integer
              example: 1870
            hora_inicio:
              type: string
              example: "00:00:00"
            hora_fin:
              type: string
              example: "23:00:00"
            idLinea:
              type: integer
              example: 1
            idProceso:
              type: integer
              example: 1
            aplica_almuerzo:
              type: boolean
              example: 1
            aplica_cena:
              type: boolean
              example: 1
            aplica_transporte:
              type: boolean
              example: 1
            observacion_transporte:
              type: string
              example: "observacion"
            fecha:
              type: string
              example: "2026-04-30"
            idCentro:
              type: int
              example: 1
            badgeNumber:
              type: int
              example: 1111
    responses:
      200:
        description: Registro creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    registro = Registro_Service.createRegistro_service(db, data)

    return jsonify(registro)

@registro_api_bp.route("/updateRegistro", methods=["POST"])
@login_required
@permiso_requerido("registro.editar")
def updateRegistro():
    """
    Modificar un registro
    ---
    tags:
      - Registro
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRegistro:
              type: integer
              example: 1
            idEmpleado:
              type: integer
              example: 1
            hora_inicio:
              type: string
              example: "2026-04-30 00:00:00"
            hora_fin:
              type: string
              example: "2026-04-30 00:00:00"
            idLinea:
              type: integer
              example: 1
            idProceso:
              type: integer
              example: 1
            aplica_almuerzo:
              type: boolean
              example: 1
            aplica_cena:
              type: boolean
              example: 1
            aplica_transporte:
              type: boolean
              example: 1
            observacion_transporte:
              type: string
              example: "observacion"
            fecha:
              type: string
              example: "2026-04-30"
            idCentro:
              type: int
              example: 1
            badgeNumber:
              type: int
              example: 1111
    responses:
      200:
        description: Registro modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    registro = Registro_Service.updateRegistro_service(db, data)

    return jsonify(registro)

@registro_api_bp.route("/deleteRegistro", methods=["POST"])
@login_required
@permiso_requerido("registro.eliminar")
def deleteRegistro():
    """
    Eliminar un registro
    ---
    tags:
      - Registro
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idRegistro:
              type: integer
              example: 1
    responses:
      200:
        description: Registro eliminado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    registro = Registro_Service.deleteRegistro_service(db, data)

    return jsonify(registro)