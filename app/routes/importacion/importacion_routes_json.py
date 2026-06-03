from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.api.importacion.importacion_service import Importacion_Service
from app.api.marcaje.marcaje_service import Marcaje_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

importacion_json_bp = Blueprint("importacion_json_pb", __name__)

@importacion_json_bp.route("/get_importaciones", methods=["GET"])
@login_required
@permiso_requerido("importacion.ver")
def get_importaciones():
    data = Importacion_Service.getImportaciones_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@importacion_json_bp.route("/create_importacion", methods=["POST"])
@login_required
@permiso_requerido("importacion.crear")
def create_importacion():
    archivo = request.files.get("archivo")

    if not archivo:
        return jsonify({
            "success": False,
            "message": "Debe seleccionar un archivo"
        }), 400
    
    data = {
        "nombre_archivo": archivo.filename,
        "idUsuario": current_user.id
    }
    
    idImportacion = Importacion_Service.createImportacion_service(db, data)

    resultado = Marcaje_Service.importar_excel_service(
        db,
        archivo
    )

    Importacion_Service.cerrarImportacion_service(
        db,
        idImportacion,
        resultado["registros"]
    )

    return jsonify({
    "success": True,
    "importacion": idImportacion,
    "registros": resultado["registros"]
})
    