from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

departamento_template_bp = Blueprint(
    "departamento_template",
    __name__,
    template_folder="../../templates"
)

@departamento_template_bp.route("/crearDepartamento")
@login_required
def crearDepartamento_template():
    departamentos = Departamento_Service.getDepartamentos_service(db)
        
    return render_template(
        f"departamento/crearDepartamento.html", 
        departamentos = departamentos,
        )

@departamento_template_bp.route("/listaDepartamentos")
@login_required
def listaDepartamentos_template():
    departamentos = Departamento_Service.getDepartamentos_service(db)
        
    return render_template(
        f"departamento/listaDepartamentos.html", 
        departamentos = departamentos, 
    )

