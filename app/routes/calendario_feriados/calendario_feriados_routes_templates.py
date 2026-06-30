from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.calendario_feriados.calendario_feriados_service import Feriado_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

feriado_template_bp = Blueprint(
    "feriado_template",
    __name__,
    template_folder="../../templates"
)

@feriado_template_bp.route("/crearFeriado")
@login_required
@permiso_requerido("feriado.crear")
def crearFeriado_template():
    feriados = Feriado_Service.getFeriados_service(db)

    return render_template(
        f"calendario_feriados/crearFeriado.html", 
        feriados = feriados,
    )

@feriado_template_bp.route("/listaFeriados")
@login_required
@permiso_requerido("feriado.ver")
def listaFeriados_template():
    feriados = Feriado_Service.getFeriados_service(db)
            
    return render_template(
        f"calendario_feriados/listaFeriados.html", 
        feriados = feriados,
    )

