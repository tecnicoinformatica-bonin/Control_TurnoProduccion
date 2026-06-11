import platform

from flask import Blueprint, jsonify, request, send_file

import os
import subprocess
import tempfile

from flask_login import login_required

from app.api.autorizacion.autorizacion_service import Autorizacion_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro.registro_service import Registro_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db
from app.reports.excel.programacion_report import (generar_reporte_programacion)
from app.reports.excel.horas_extra_autorizadas_report import (generar_reporte_horas_extra_autorizadas, generar_reporte_horas_extra_pendientes, generar_reporte_resumen_horas_autorizadas, generar_reporte_horas_autorizadas_por_empleado_linea)

reports_json_bp = Blueprint("reports_json_pb", __name__)

@reports_json_bp.route("/programacion/descargar_programacion/<int:idProgramacion>/isPDF=<int:isPDF>")
@login_required
@permiso_requerido("programacion.ver")
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

@reports_json_bp.route("/autorizacion/descargar_autorizacion_horas_extra/<string:from_date>/<string:to_date>/<int:idDepartment>/isPDF=<int:isPDF>")
@login_required
# @permiso_requerido("programacion.ver")
def descargar_autorizacion_horas_extra(from_date, to_date, idDepartment, isPDF):
    encabezado_detalles, detalles = Autorizacion_Service.get_detalles_autorizaciones_reporte_service(db, from_date, to_date, idDepartment)

    archivo = generar_reporte_horas_extra_autorizadas(encabezado_detalles, detalles)

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
            download_name=f"Autorizacion_horas_extra_{from_date}_{to_date}.pdf",
            mimetype="application/pdf"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Autorizacion_horas_extra_{from_date}_{to_date}.xlsm",
        mimetype=(
            "application/vnd.ms-excel.sheet.macroEnabled.12"
        )
    )

@reports_json_bp.route("/autorizacion/descargar_horas_extra_pendientes/<string:from_date>/<string:to_date>/<int:idDepartment>/isPDF=<int:isPDF>")
@login_required
# @permiso_requerido("programacion.ver")
def descargar_horas_extra_pendientes(from_date, to_date, idDepartment, isPDF):
    encabezado_detalles, detalles = Autorizacion_Service.get_detalles_pendientes_reporte_service(db, from_date, to_date, idDepartment)

    archivo = generar_reporte_horas_extra_pendientes(encabezado_detalles, detalles)

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
            download_name=f"Pendientes_de_autorizacion_{from_date}_{to_date}.pdf",
            mimetype="application/pdf"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Pendientes_de_autorizacion_{from_date}_{to_date}.xlsm",
        mimetype=(
            "application/vnd.ms-excel.sheet.macroEnabled.12"
        )
    )

@reports_json_bp.route("/autorizacion/descargar_resumen_horas_autorizadas/<string:from_date>/<string:to_date>/<int:idDepartment>/isPDF=<int:isPDF>")
@login_required
# @permiso_requerido("programacion.ver")
def descargar_resumen_horas_autorizadas(from_date, to_date, idDepartment, isPDF):
    encabezado_detalles, detalles = Autorizacion_Service.get_resumen_horas_autorizadas_reporte_service(db, from_date, to_date, idDepartment)

    archivo = generar_reporte_resumen_horas_autorizadas(encabezado_detalles, detalles)

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
            download_name=f"Resumen_horas_autorizadas_{from_date}_{to_date}.pdf",
            mimetype="application/pdf"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Resumen_horas_autorizadas_{from_date}_{to_date}.xlsm",
        mimetype=(
            "application/vnd.ms-excel.sheet.macroEnabled.12"
        )
    )

@reports_json_bp.route("/autorizacion/descargar_horas_autorizadas_por_empleado_linea/<string:from_date>/<string:to_date>/<int:idDepartment>/isPDF=<int:isPDF>")
@login_required
# @permiso_requerido("programacion.ver")
def horas_autorizadas_por_empleado_linea(from_date, to_date, idDepartment, isPDF):
    encabezado_detalles, detalles = Autorizacion_Service.get_horas_autorizadas_por_empleado_linea_service(db, from_date, to_date, idDepartment)

    archivo = generar_reporte_horas_autorizadas_por_empleado_linea(encabezado_detalles, detalles)

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
            download_name=f"Horas_por_empleado_linea_{from_date}_{to_date}.pdf",
            mimetype="application/pdf"
        )

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"Horas_por_empleado_linea_{from_date}_{to_date}.xlsm",
        mimetype=(
            "application/vnd.ms-excel.sheet.macroEnabled.12"
        )
    )
