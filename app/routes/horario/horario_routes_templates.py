from flask import Blueprint, render_template, abort
from flask_login import login_required

from app.api.horario.horario_service import Horario_Service
from app.api.departamento.departamento_service import Departamento_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

horario_template_bp = Blueprint(
    "horario_template",
    __name__,
    template_folder="../../templates"
)

@horario_template_bp.route("/crearHorario")
@login_required
@permiso_requerido("horario.crear")
def crearHorario_template():
    horarios = Horario_Service.getHorarios_service(db)

    for h in horarios:
        total_segundos_inicio = int(h["hora_inicio"].total_seconds())
        horas_inicio = total_segundos_inicio // 3600
        minutos_inicio = (total_segundos_inicio % 3600) // 60

        total_segundos_fin = int(h["hora_fin"].total_seconds())
        horas_fin = total_segundos_fin // 3600
        minutos_fin = (total_segundos_fin % 3600) // 60

        h["hora_inicio"] = f"{horas_inicio:02d}:{minutos_inicio:02d}"
        h["hora_fin"] = f"{horas_fin:02d}:{minutos_fin:02d}"

    return render_template(
        f"horario/crearHorario.html", 
        horarios = horarios,
    )

@horario_template_bp.route("/listaHorarios")
@login_required
@permiso_requerido("horario.ver")
def listaHorarios_template():
    horarios = Horario_Service.getHorarios_service(db)
    
    for h in horarios:
        total_segundos_inicio = int(h["hora_inicio"].total_seconds())
        horas_inicio = total_segundos_inicio // 3600
        minutos_inicio = (total_segundos_inicio % 3600) // 60

        total_segundos_fin = int(h["hora_fin"].total_seconds())
        horas_fin = total_segundos_fin // 3600
        minutos_fin = (total_segundos_fin % 3600) // 60

        h["hora_inicio"] = f"{horas_inicio:02d}:{minutos_inicio:02d}"
        h["hora_fin"] = f"{horas_fin:02d}:{minutos_fin:02d}"
            
    return render_template(
        f"horario/listaHorarios.html", 
        horarios = horarios,
    )

