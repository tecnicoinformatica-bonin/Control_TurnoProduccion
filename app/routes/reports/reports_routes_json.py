import platform

from flask import Blueprint, jsonify, request, send_file

import os
import subprocess
import tempfile

from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro.registro_service import Registro_Service
from app.extensions.db import db
from app.reports.excel.programacion_report import (generar_reporte_programacion)

reports_json_bp = Blueprint("reports_json_pb", __name__)

@reports_json_bp.route("/programacion/descargar_programacion/<int:idProgramacion>/isPDF=<int:isPDF>")
def descargar_programacion(idProgramacion, isPDF):
    programacion_detalles = Programacion_Service.getDetallesProgramacionByIdProgramacion_service(db, idProgramacion)
    registros_detalles = Registro_Service.getDetalleRegistrosByProgramacion_service(db, idProgramacion)
    
    fecha = programacion_detalles["fecha"]

    archivo = generar_reporte_programacion(programacion_detalles, registros_detalles)

    isPDF = bool(isPDF)

    if isPDF:
        temp_dir = tempfile.mkdtemp()

        ruta_excel = os.path.join(temp_dir, "reporte.xlsm")
        ruta_pdf = os.path.join(temp_dir, "reporte.pdf")

        with open(ruta_excel, "wb") as f:
            f.write(archivo.getbuffer())

        if platform.system() == "Windows":
            libreoffice_cmd = r"C:\Program Files\LibreOffice\program\soffice.exe"
        else:
            libreoffice_cmd = "/usr/bin/libreoffice"

        comando = [
            libreoffice_cmd,
            "--headless",
            "--convert-to",
            "pdf",
            ruta_excel,
            "--outdir",
            temp_dir
        ]

        subprocess.run(
            comando, 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return send_file(
            ruta_pdf,
            as_attachment=True,
            download_name=f"Programacion_{fecha}.pdf",
            mimetype="application/pdf"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Programacion_{fecha}.xlsm",
        mimetype=(
            "application/vnd.ms-excel.sheet.macroEnabled.12"
        )
    )

