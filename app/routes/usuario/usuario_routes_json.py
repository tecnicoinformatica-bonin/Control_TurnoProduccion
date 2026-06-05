from datetime import datetime

from flask import Blueprint, jsonify, request, session
from flask_login import login_required, login_user
from app.api.usuario.usuario_model import Usuario_Rutas
from app.api.usuario.usuario_repository import UsuarioRepository
from app.api.usuario.usuario_service import Usuario_Service
from app.core.auth.permiso_requerido_decorator import permiso_requerido
from app.extensions.db import db

usuario_json_bp = Blueprint("usuario_json_bp", __name__)

@usuario_json_bp.route("/get_usuarios", methods=["GET"])
@login_required
def get_usuarios():
    data = Usuario_Service.getUsuarios_service(db)
    if not data:
        return jsonify([]), 200

    return jsonify(data), 200

@usuario_json_bp.route("/reauth", methods=["POST"])
def reauth():

    data = request.get_json()

    dataUser = {
        "username": data.get("username"),
        "password": data.get("password"),
    }
    print(dataUser)

    usuario = Usuario_Service.login_service(db, dataUser)
    if "error" in usuario:
        return jsonify({
            "success": False,
            "message": "Credenciales inválidas"
        }), 401
    
    user = Usuario_Service.getUsuario_login_service(db, usuario["idUsuario"])

    login_user(user)

    session['ultima_actividad'] = datetime.now().isoformat()

    return jsonify({
        "success": True
    })