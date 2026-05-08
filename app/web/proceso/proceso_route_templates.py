from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.proceso.proceso_service import Proceso_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

proceso_template_bp = Blueprint(
    "proceso_template",
    __name__,
    template_folder="../../templates"
)

@proceso_template_bp.route("/crearProceso")
@login_required
def crearProceso_template():
    procesos = Proceso_Service.getProcesos_service(db)
    departamentos = Departamento_Service.getDepartamentosSuperiores_service(db);
        
    return render_template(
        f"proceso/crearProceso.html", 
        procesos = procesos,
        departamentos = departamentos,
    )

@proceso_template_bp.route("/listaProcesos")
@login_required
def listaProcesos_template():
    procesos = Proceso_Service.getProcesos_service(db)
    departamentos = Departamento_Service.getDepartamentosSuperiores_service(db);
            
    return render_template(
        f"proceso/listaProcesos.html", 
        procesos = procesos,
        departamentos = departamentos,
    )

