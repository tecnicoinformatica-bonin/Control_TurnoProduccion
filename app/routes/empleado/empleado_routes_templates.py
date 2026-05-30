from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.linea.linea_service import Linea_Service
from app.api.proceso.proceso_service import Proceso_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

empleado_template_bp = Blueprint(
    "empleado_template",
    __name__,
    template_folder="../../templates"
)

@empleado_template_bp.route("/crearEmpleado")
@login_required
@permiso_requerido("empleado.crear")
def crearEmpleado_template():
    empleados = Empleado_Service.getEmpleados_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
    lineas = Linea_Service.getLineas_service(db)
    procesos = Proceso_Service.getProcesos_service(db)
        
    return render_template(
        f"empleado/crearEmpleado.html", 
        empleados = empleados,
        departamentos = departamentos,
        centros_de_costo = centros_de_costo,
        lineas = lineas,
        procesos = procesos,
    )   

@empleado_template_bp.route("/listaEmpleados")
@login_required
@permiso_requerido("empleado.ver")
def listaEmpleados_template():
    empleados = Empleado_Service.getEmpleados_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
    lineas = Linea_Service.getLineas_service(db)
    procesos = Proceso_Service.getProcesos_service(db)
            
    return render_template(
        f"empleado/listaEmpleados.html", 
        empleados = empleados,
        departamentos = departamentos,
        centros_de_costo = centros_de_costo,
        lineas = lineas,
        procesos = procesos,
    )

