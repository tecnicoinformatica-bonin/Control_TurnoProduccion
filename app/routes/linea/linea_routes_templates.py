from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.linea.linea_service import Linea_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

linea_template_bp = Blueprint(
    "linea_template",
    __name__,
    template_folder="../../templates"
)

@linea_template_bp.route("/crearLinea")
@login_required
@permiso_requerido("linea.crear")
def crearLinea_template():
    return render_template(
        f"linea/crearLinea.html", 
    )

@linea_template_bp.route("/listaLineas")
@login_required
@permiso_requerido("linea.ver")
def listaLineas_template():
    lineas = Linea_Service.getLineas_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
            
    return render_template(
        f"linea/listaLineas.html", 
        lineas = lineas,
        departamentos = departamentos,
    )

