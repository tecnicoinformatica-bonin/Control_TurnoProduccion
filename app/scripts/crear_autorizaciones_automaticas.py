from datetime import datetime, timedelta

import pytz

from app import create_app
from app.api.departamento.departamento_service import Departamento_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.extensions.db import db

from app.api.autorizacion.autorizacion_service import Autorizacion_Service

app = create_app()

with app.app_context():
    try:
        tz = pytz.timezone("America/Guatemala")
        fecha_actual = datetime.now(tz)
        ayer = fecha_actual - timedelta(days=1)
        ayer_str = ayer.strftime("%Y-%m-%d")

        autorizaciones = 0
        daysCount = 1

        departamentos = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)

        while daysCount < 7: # 7 es para una semana antes
            day = fecha_actual - timedelta(days=daysCount)
            day_str = day.strftime("%Y-%m-%d")

            for d in departamentos:
                autorizaciones += Autorizacion_Service.create_autorizacion_automatica(db, day_str, d["idDepartment"])
            
            daysCount += 1

        print("=====================================")
        print("CREACIÓN AUTOMÁTICA DE AUTORIZACIONES")
        print("=====================================")
        print(f"Autorizaciones creadas: {autorizaciones}")

    except Exception as e:
        print("ERROR EN AUTORIZACIONES AUTOMÁTICAS")
        print(str(e))