from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.linea.linea_service import Linea_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

linea_template_bp = Blueprint(
    "linea_template",
    __name__,
    template_folder="../../templates"
)

@linea_template_bp.route("/crearLinea")
@login_required
def crearLinea_template():
    lineas = Linea_Service.getLineas_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
        
    return render_template(
        f"linea/crearLinea.html", 
        lineas = lineas,
        departamentos = departamentos,
    )

@linea_template_bp.route("/listaLineas")
@login_required
def listaLineas_template():
    lineas = Linea_Service.getLineas_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
            
    return render_template(
        f"linea/listaLineas.html", 
        lineas = lineas,
        departamentos = departamentos,
    )

