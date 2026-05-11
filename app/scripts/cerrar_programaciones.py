from app import create_app
from app.extensions.db import db

from app.api.programacion.programacion_service import Programacion_Service


app = create_app()


with app.app_context():

    try:
        cantidad = Programacion_Service.cerrar_programaciones_vencidas_service(db)

        print("====================================")
        print("CIERRE AUTOMÁTICO DE PROGRAMACIONES")
        print("====================================")
        print(f"Programaciones cerradas: {cantidad}")

    except Exception as e:
        print("ERROR EN CIERRE AUTOMÁTICO")
        print(str(e))