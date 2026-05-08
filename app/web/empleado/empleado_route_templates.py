from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

empleado_template_bp = Blueprint(
    "empleado_template",
    __name__,
    template_folder="../../templates"
)

@empleado_template_bp.route("/crearEmpleado")
@login_required
def crearEmpleado_template():
    empleados = Empleado_Service.getEmpleados_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
        
    return render_template(
        f"empleado/crearEmpleado.html", 
        empleados = empleados,
        departamentos = departamentos,
        centros_de_costo = centros_de_costo,
    )   

@empleado_template_bp.route("/listaEmpleados")
@login_required
def listaEmpleados_template():
    empleados = Empleado_Service.getEmpleados_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
            
    return render_template(
        f"empleado/listaEmpleados.html", 
        empleados = empleados,
        departamentos = departamentos,
        centros_de_costo = centros_de_costo,
    )

