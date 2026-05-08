from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.ruta.ruta_service import Ruta_Service
from app.extensions.db import db

ruta_template_bp = Blueprint(
    "ruta_template",
    __name__,
    template_folder="../../templates"
)

@ruta_template_bp.route("/crearRuta")
@login_required
def crearRuta_template():
    rutas = Ruta_Service.getRutas_service(db)
        
    return render_template(
        f"ruta/crearRuta.html", 
        rutas = rutas,
    )

@ruta_template_bp.route("/listaRutas")
@login_required
def listaRutas_template():
    rutas = Ruta_Service.getRutas_service(db)
            
    return render_template(
        f"ruta/listaRutas.html", 
        rutas = rutas,
    )

