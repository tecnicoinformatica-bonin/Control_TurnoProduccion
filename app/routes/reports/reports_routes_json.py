
from flask import Blueprint, jsonify, request, send_file

from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro.registro_service import Registro_Service
from app.extensions.db import db
from app.reports.excel.programacion_report import (generar_reporte_programacion)

reports_json_bp = Blueprint("reports_json_pb", __name__)

@reports_json_bp.route("/programacion/descargar_programacion/<int:idProgramacion>")
def descargar_programacion(idProgramacion):
    programacion_detalles = Programacion_Service.getDetallesProgramacionByIdProgramacion_service(db, idProgramacion)
    registros_detalles = Registro_Service.getDetalleRegistrosByProgramacion_service(db, idProgramacion)
    
    fecha = programacion_detalles["fecha"]

    archivo = generar_reporte_programacion(programacion_detalles, registros_detalles)

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Programacion_{fecha}.xlsx",
        mimetype=(
            "application/"
            "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    )

