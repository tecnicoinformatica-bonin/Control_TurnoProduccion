from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.api.empleado.empleado_service import Empleado_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

empleado_api_bp = Blueprint("empleado_api_pb", __name__)

@empleado_api_bp.route("/getEmpleados", methods=["GET"])
@login_required
@permiso_requerido("empleado.ver")
def getEmpleados():
    """
    Obtener empleados
    ---
    tags:
      - Empleado
    responses:
      200:
        description: Lista de empleados
    """
    empleados = Empleado_Service.getEmpleados_service(db)

    return jsonify(empleados)

@empleado_api_bp.route("/getActiveEmpleados", methods=["GET"])
@login_required
@permiso_requerido("empleado.ver")
def getActiveEmpleados():
    """
    Obtener empleados activos
    ---
    tags:
      - Empleado
    responses:
      200:
        description: Lista de empleados activos
    """
    empleados = Empleado_Service.getActiveEmpleados_service(db)

    return jsonify(empleados)

@empleado_api_bp.route("/createEmpleado", methods=["POST"])
@login_required
@permiso_requerido("empleado.crear")
def createEmpleado():
    """
    Crear un nuevo empleado
    ---
    tags:
      - Empleado
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            idEmpleado:
              type: integer
              example: 1870
            badgeNumber:
              type: integer
              example: 1870
            firstName:
              type: string
              example: name
            secondName:
              type: string
              example: name
            lastName:
              type: string
              example: name
            lastName2:
              type: string
              example: name
            position:
              type: string
              example: puesto
            idDepartment:
              type: integer
              example: 1
            activo:
              type: boolean
              example: 1
            idCentro:
              type: integer
              example: 1
            idLinea:
              type: integer
              example: 1
            idProceso:
              type: integer
              example: 1
            idHorario:
              type: integer
              example: 1
    responses:
      200:
        description: empleado creado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    empleado = Empleado_Service.createEmpleado_service(db, data)

    return jsonify(empleado)

@empleado_api_bp.route("/updateEmpleado", methods=["POST"])
@login_required
@permiso_requerido("empleado.editar")
def updateEmpleado():
    """
    Modificar un empleado
    ---
    tags:
      - Empleado
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            oldIdEmpleado:
              type: integer
              example: 1870
            oldBadgeNumber:
              type: integer
              example: 1870
            idEmpleado:
              type: integer
              example: 1870
            badgeNumber:
              type: integer
              example: 1870
            firstName:
              type: string
              example: name
            secondName:
              type: string
              example: name
            lastName:
              type: string
              example: name
            lastName2:
              type: string
              example: name
            position:
              type: string
              example: puesto
            idDepartment:
              type: integer
              example: 1
            activo:
              type: boolean
              example: 1
            idCentro:
              type: integer
              example: 1
            idLinea:
              type: integer
              example: 1
            idProceso:
              type: integer
              example: 1
            idHorario:
              type: integer
              example: 1
    responses:
      200:
        description: empleado modificado correctamente
    """

    # La siguiente línea es para que el endpoint funcione desde Swagger o Postman
    data = request.get_json(silent=True)
    
    # Si la info viene desde un formulario de HTML, entonces esta validación es importante.
    if not data:
        data = request.form

    empleado = Empleado_Service.updateEmpleado_service(db, data)

    return jsonify(empleado)