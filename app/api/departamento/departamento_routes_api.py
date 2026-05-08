from flask import Blueprint, jsonify, request
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

departamento_api_bp = Blueprint("departamento_api_pb", __name__)

@departamento_api_bp.route("/getDepartamentos", methods=["GET"])
def get_departamentos():
    """
    Obtener departamentos
    ---
    tags:
      - Departamento
    responses:
      200:
        description: Lista de departamentos
    """
    departamentos = Departamento_Service.getDepartamentos_service(db)

    return jsonify(departamentos)

@departamento_api_bp.route("/getDepartamentos_aplica_horas_extra", methods=["GET"])
def get_departamentos_aplica_horas_extra():
    """
    Obtener departamentos en los que aplican horas extra
    ---
    tags:
      - Departamento
    responses:
      200:
        description: Lista de departamentos que aplican a horas extra
    """
    departamentos = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)

    return jsonify(departamentos)

@departamento_api_bp.route("/createDepartamento", methods=["POST"])
def createDepartamento():
    """
    Crear un nuevo departamento
    ---
    tags:
      - Departamento
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Bonin"
            aplica_horas_extra:
              type: boolean
              example: 1
    responses:
      200:
        description: Departamento creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    departamento = Departamento_Service.createDepartamento_service(db, data)

    return jsonify(departamento)

@departamento_api_bp.route("/deleteDepartamento", methods=["POST"])
def updateDepartamento():
    """
    Eliminar un departamento
    ---
    tags:
      - Departamento
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idDepartment:
              type: integer
              example: 1
    responses:
      200:
        description: Departamento eliminado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    departamento = Departamento_Service.deleteDepartamento_service(db, data)

    return jsonify(departamento)