from datetime import datetime

import pandas as pd
import pytz

from app.api.marcaje.marcaje_repository import MarcajeRepository
from app.extensions.slugify import Slugify

class Marcaje_Service():
    @staticmethod
    def createMarcaje_service(db, data):
        try:
            idEmpleado = data.get("idEmpleado")
            nombre_empleado = data.get("nombre_empleado")
            departamento = data.get("departamento")
            area = data.get("area")
            dia = data.get("dia")
            fecha = data.get("fecha")
            entrada_garita = data.get("entrada_garita")
            entrada_area = data.get("entrada_area")
            salida_area = data.get("salida_area")
            salida_garita = data.get("salida_garita")
            hora_simple = data.get("hora_simple")
            hora_doble = data.get("hora_doble")
            total_horas = data.get("total_horas")
            horario_inicio = data.get("horario_inicio")
            horario_fin = data.get("horario_fin")
            
            required_fields = {
                "idEmpleado": idEmpleado,
                "nombre_empleado": nombre_empleado,
                "departamento": departamento,
                "area": area,
                "dia": dia,
                "fecha": fecha,
                "entrada_garita": entrada_garita,
                "entrada_area": entrada_area,
                "salida_area": salida_area,
                "salida_garita": salida_garita,
                "hora_simple": hora_simple,
                "hora_doble": hora_doble,
                "total_horas": total_horas,
                "horario_inicio": horario_inicio,
                "horario_fin": horario_fin
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return MarcajeRepository.createMarcaje(
                db,
                idEmpleado,
                nombre_empleado,
                departamento,
                area,
                dia,
                fecha,
                entrada_garita,
                entrada_area,
                salida_area,
                salida_garita,
                hora_simple,
                hora_doble,
                total_horas,
                horario_inicio,
                horario_fin,
            )
        
        except Exception as ex:
            return {"error": f"No se pudo crear el marcaje. {str(ex)}"}
        
    @staticmethod
    def importar_excel_service(db,archivo):
        df = pd.read_excel(archivo)

        df = df.where(
            pd.notnull(df),
            None
        )

        registros = 0

        for _, row in df.iterrows():
            fecha = pd.to_datetime(
                row["fecha"],
                dayfirst=True
            ).date()

            # for columna, valor in row.items():
            #     if pd.isna(valor):
            #         print(f"NaN encontrado -> {columna}")

            row = row.where(pd.notnull(row), None)

            # Timezone de Guatemala
            tz = pytz.timezone("America/Guatemala")

            # Hora actual REAL 
            fecha_importacion = datetime.now(tz)

            resultado = MarcajeRepository.createMarcaje(
                db,
                row["id_empleado"],
                row["nombre_empleado"],
                row["departamento"],
                row["area"],
                row["dia"],
                fecha,
                row["entrada_garita"],
                row["entrada_area"],
                row["salida_area"],
                row["salida_garita"],
                row["hora_simple"],
                row["hora_doble"],
                row["total_horas"],
                row["horario_inicio"],
                row["horario_fin"],
                fecha_importacion
            )

            registros += 1

            if "error" in resultado:
                print(f"ERROR: {resultado["error"]}")

        db.connection.commit()
        
        return {
            "success": True,
            "registros": registros
        }
