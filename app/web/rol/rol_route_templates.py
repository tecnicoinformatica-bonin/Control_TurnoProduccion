from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.rol.rol_service import Rol_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.api.rol_ruta.rol_ruta_service import Rol_Ruta_Service
from app.api.ruta.ruta_service import Ruta_Service
from app.extensions.db import db

rol_template_bp = Blueprint(
    "rol_template",
    __name__,
    template_folder="../../templates"
)

@rol_template_bp.route("/crearRol")
@login_required
def crearRol_template():
    roles = Rol_Service.getRoles_service(db)
    rutas = Ruta_Service.getRutasDESC_service(db)
    rol_rutas = Rol_Ruta_Service.getRol_Rutas_service(db)
        
    return render_template(
        f"rol/crearRol.html", 
        roles = roles,
        rutas = rutas,
        rol_rutas = rol_rutas,
    )

@rol_template_bp.route("/listaRoles")
@login_required
def listaRoles_template():
    roles = Rol_Service.getRoles_service(db)
    rol_rutas = Rol_Ruta_Service.getRol_Rutas_service(db)
    rutas = Ruta_Service.getRutas_service(db)
            
    return render_template(
        f"rol/listaRoles.html", 
        roles = roles,
        rutas = rutas,
        rol_rutas = rol_rutas,
    )

