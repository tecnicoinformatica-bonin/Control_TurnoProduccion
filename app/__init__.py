from flask import Flask, redirect, url_for, session, request
from datetime import datetime, timedelta
from config import DevelopmentConfig
from flask_login import LoginManager, current_user
from app.api.usuario.usuario_service import Usuario_Service

from app.extensions.db import db
from app.extensions.swagger import init_swagger

# API
from app.api import api_bp
from app.routes.centro_de_costo.centro_de_costo_routes_api import centro_de_costo_api_bp
from app.routes.departamento.departamento_routes_api import departamento_api_bp
from app.routes.empleado.empleado_routes_api import empleado_api_bp
from app.routes.linea.linea_routes_api import linea_api_bp
from app.routes.permiso.permiso_routes_api import permiso_api_bp
from app.routes.proceso.proceso_routes_api import proceso_api_bp
from app.routes.programacion.programacion_routes_api import programacion_api_bp
from app.routes.registro.registro_routes_api import registro_api_bp
from app.routes.rol.rol_routes_api import rol_api_bp
from app.routes.rol_ruta.rol__ruta_routes_api import rol_ruta_api_bp
from app.routes.ruta.ruta_routes_api import ruta_api_bp
from app.routes.usuario.usuario_routes_api import usuario_api_bp
from app.routes.usuario_permiso.usuario_permiso_routes_api import usuario_permiso_api_bp
from app.routes.usuario_rol.usuario_rol_routes_api import usuario_rol_api_bp

# WEB TEMPLATES
from app.routes.centro_de_costo.centro_de_costo_routes_templates import centro_de_costo_template_bp
from app.routes.departamento.departamento_routes_templates import departamento_template_bp
from app.routes.empleado.empleado_routes_templates import empleado_template_bp
from app.routes.linea.linea_routes_templates import linea_template_bp
from app.routes.permiso.permiso_routes_templates import permiso_template_bp
from app.routes.proceso.proceso_routes_templates import proceso_template_bp
from app.routes.programacion.programacion_routes_templates import programacion_template_bp
from app.routes.registro.registro_routes_templates import registro_template_bp
from app.routes.rol.rol_routes_templates import rol_template_bp
from app.routes.rol_ruta.rol_ruta_routes_templates import rol_ruta_template_bp
from app.routes.ruta.ruta_routes_templates import ruta_template_bp
from app.routes.usuario.usuario_routes_templates import usuario_template_bp
from app.routes.usuario_permiso.usuario_permiso_routes_templates import usuario_permiso_template_bp
from app.routes.usuario_rol.usuario_rol_routes_templates import usuario_rol_template_bp
from app.routes.home.home_routes_templates import home_template_bp

# WEB LOGIC
from app.routes.centro_de_costo.centro_de_costo_routes_web import centro_de_costo_web_bp
from app.routes.departamento.departamento_routes_web import departamento_web_bp
from app.routes.empleado.empleado_routes_web import empleado_web_bp
from app.routes.linea.linea_routes_web import linea_web_bp
from app.routes.permiso.permiso_routes_web import permiso_web_bp
from app.routes.proceso.proceso_routes_web import proceso_web_bp
from app.routes.programacion.programacion_routes_web import programacion_web_bp
from app.routes.registro.registro_routes_web import registro_web_bp
from app.routes.rol.rol_routes_web import rol_web_bp
from app.routes.rol_ruta.rol_ruta_routes_web import rol_ruta_web_bp
from app.routes.ruta.ruta_routes_web import ruta_web_bp
from app.routes.usuario.usuario_routes_web import usuario_web_bp
from app.routes.usuario_permiso.usuario_permiso_routes_web import usuario_permiso_web_bp
from app.routes.usuario_rol.usuario_rol_routes_web import usuario_rol_web_bp

# blueprints for JSON APIS
from app.routes.centro_de_costo.centro_de_costo_routes_json import centro_de_costo_json_bp
from app.routes.empleado.empleado_routes_json import empleado_json_bp
from app.routes.linea.linea_routes_json import linea_json_bp
from app.routes.permiso.permiso_routes_json import permiso_json_bp
from app.routes.proceso.proceso_routes_json import proceso_json_bp
from app.routes.programacion.programacion_routes_json import programacion_json_bp
from app.routes.registro.registro_routes_json import registro_json_bp
from app.routes.reports.reports_routes_json import reports_json_bp

# Login Manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    init_swagger(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "usuario_template.login"
    """ login_manager.login_message = None """

    # Manejo de tiempo por inactividad
    app.permanent_session_lifetime = timedelta(minutes=60)

    @app.before_request
    def controlar_inactividad():
        rutas_excluidas = [
            "usuario_template.login",
            "static"
        ]

        if request.endpoint in rutas_excluidas:
            return

        if current_user.is_authenticated:
            ahora = datetime.now()

            if 'ultima_actividad' in session:
                ultima = datetime.fromisoformat(session['ultima_actividad'])

                if ahora - ultima > timedelta(minutes=60):
                    session.clear()
                    return redirect(url_for("usuario_template.login"))

            session['ultima_actividad'] = ahora.isoformat()

    
    # Registro de blueprints
    # API
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(centro_de_costo_api_bp, url_prefix="/api/centro_de_costo")
    app.register_blueprint(departamento_api_bp, url_prefix="/api/departamento")
    app.register_blueprint(empleado_api_bp, url_prefix="/api/empleado")
    app.register_blueprint(linea_api_bp, url_prefix="/api/linea")
    app.register_blueprint(permiso_api_bp, url_prefix="/api/permiso")
    app.register_blueprint(proceso_api_bp, url_prefix="/api/proceso")
    app.register_blueprint(programacion_api_bp, url_prefix="/api/programacion")
    app.register_blueprint(registro_api_bp, url_prefix="/api/registro")
    app.register_blueprint(rol_api_bp, url_prefix="/api/rol")
    app.register_blueprint(rol_ruta_api_bp, url_prefix="/api/rol_ruta")
    app.register_blueprint(ruta_api_bp, url_prefix="/api/ruta")
    app.register_blueprint(usuario_api_bp, url_prefix="/api/usuario")
    app.register_blueprint(usuario_permiso_api_bp, url_prefix="/api/usuario_permiso")
    app.register_blueprint(usuario_rol_api_bp, url_prefix="/api/usuario_rol")

    # WEB TEMPLATES
    app.register_blueprint(centro_de_costo_template_bp, url_prefix="/template/centro_de_costo")
    app.register_blueprint(departamento_template_bp, url_prefix="/template/departamento")
    app.register_blueprint(empleado_template_bp, url_prefix="/template/empleado")
    app.register_blueprint(linea_template_bp, url_prefix="/template/linea")
    app.register_blueprint(permiso_template_bp, url_prefix="/template/permiso")
    app.register_blueprint(proceso_template_bp, url_prefix="/template/proceso")
    app.register_blueprint(programacion_template_bp, url_prefix="/template/programacion")
    app.register_blueprint(registro_template_bp, url_prefix="/template/registro")
    app.register_blueprint(rol_template_bp, url_prefix="/template/rol")
    app.register_blueprint(rol_ruta_template_bp, url_prefix="/template/rol_ruta")
    app.register_blueprint(ruta_template_bp, url_prefix="/template/ruta")
    app.register_blueprint(usuario_template_bp, url_prefix="/template/usuario")
    app.register_blueprint(usuario_permiso_template_bp, url_prefix="/template/usuario_permiso")
    app.register_blueprint(usuario_rol_template_bp, url_prefix="/template/usuario")
    app.register_blueprint(home_template_bp, url_prefix="/template/home")

    # WEB LOGIC
    app.register_blueprint(centro_de_costo_web_bp, url_prefix="/web/centro_de_costo")
    app.register_blueprint(departamento_web_bp, url_prefix="/web/departamento")
    app.register_blueprint(empleado_web_bp, url_prefix="/web/empleado")
    app.register_blueprint(linea_web_bp, url_prefix="/web/linea")
    app.register_blueprint(permiso_web_bp, url_prefix="/web/permiso")
    app.register_blueprint(proceso_web_bp, url_prefix="/web/proceso")
    app.register_blueprint(programacion_web_bp, url_prefix="/web/programacion")
    app.register_blueprint(registro_web_bp, url_prefix="/web/registro")
    app.register_blueprint(rol_web_bp, url_prefix="/web/rol")
    app.register_blueprint(rol_ruta_web_bp, url_prefix="/web/rol_ruta")
    app.register_blueprint(ruta_web_bp, url_prefix="/web/ruta")
    app.register_blueprint(usuario_web_bp, url_prefix="/web/usuario")
    app.register_blueprint(usuario_permiso_web_bp, url_prefix="/web/usuario_permiso")
    app.register_blueprint(usuario_rol_web_bp, url_prefix="/web/usuario_rol")

    # JSON APIs
    app.register_blueprint(centro_de_costo_json_bp, url_prefix="/json/centro_de_costo")
    app.register_blueprint(empleado_json_bp, url_prefix="/json/empleado")
    app.register_blueprint(linea_json_bp, url_prefix="/json/linea")
    app.register_blueprint(permiso_json_bp, url_prefix="/json/permiso")
    app.register_blueprint(programacion_json_bp, url_prefix="/json/programacion")
    app.register_blueprint(proceso_json_bp, url_prefix="/json/proceso")
    app.register_blueprint(registro_json_bp, url_prefix="/json/registro")
    app.register_blueprint(reports_json_bp, url_prefix="/json/reports")


    @app.route("/")
    def index():
        return redirect(url_for("usuario_template.login"))
    
    return app

@login_manager.user_loader
def load_user(idUsuario):
    return Usuario_Service.getUsuario_login_service(db, idUsuario)