from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.configuracion.configuracion_service import Configuracion_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

configuracion_template_bp = Blueprint(
    "configuracion_template",
    __name__,
    template_folder="../../templates"
)

@configuracion_template_bp.route("/listaConfiguraciones")
@login_required
# @permiso_requerido("configuracion.ver")
def listaConfiguraciones_template():
    configuraciones = Configuracion_Service.getConfiguraciones_service(db)
    departamentos = Departamento_Service.getDepartamentos_service(db);
            
    return render_template(
        f"configuracion/listaConfiguraciones.html", 
        configuraciones = configuraciones,
        departamentos = departamentos,
    )

