from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.extensions.db import db

centro_de_costo_template_bp = Blueprint(
    "centro_de_costo_template",
    __name__,
    template_folder="../../templates"
)

@centro_de_costo_template_bp.route("/crearCentro_de_costo")
@login_required
def crearCentro_de_costo_template():
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db)
        
    return render_template(
        f"centro_de_costo/crearCentro_de_costo.html", 
        centros_de_costo = centros_de_costo,
        departamentos = departamentos,
    )

@centro_de_costo_template_bp.route("/listaCentros_de_costo")
@login_required
def listaCentros_de_costo_template():
    centros_de_costo = Centro_de_costo_Service.getCentros_de_costo_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
            
    return render_template(
        f"centro_de_costo/listaCentros_de_costo.html", 
        centros_de_costo = centros_de_costo,
        departamentos = departamentos,
    )

