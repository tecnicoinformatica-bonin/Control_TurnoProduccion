from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.departamento.departamento_service import Departamento_Service
from app.api.permiso.permiso_service import Permiso_Service
from app.extensions.db import db

permiso_template_bp = Blueprint(
    "permiso_template",
    __name__,
    template_folder="../../templates"
)

@permiso_template_bp.route("/crearPermiso")
@login_required
def crearPermiso_template():
    departamentos = Departamento_Service.getDepartamentos_service(db)

    return render_template(
        f"permiso/crearPermiso.html", 
        departamentos = departamentos,
    )

@permiso_template_bp.route("/listaPermisos")
@login_required
def listaPermisos_template():
    departamentos = Departamento_Service.getDepartamentos_service(db)
    permisos = Permiso_Service.getPermisos_service(db)
            
    return render_template(
        f"permiso/listaPermisos.html", 
        permisos = permisos,
        departamentos = departamentos,
    )

