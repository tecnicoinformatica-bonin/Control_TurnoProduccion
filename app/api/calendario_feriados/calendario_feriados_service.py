from flask import current_app

from app.api.calendario_feriados.calendario_feriados_repository import FeriadoRepository

class Feriado_Service():
    @staticmethod
    def getFeriados_service(db):
        try:
            data = FeriadoRepository.getFeriados(db)
            feriados = []
            for row in data:
                fecha_str = row["fecha"].strftime("%Y-%m-%d")
                feriado = {
                    "idFeriado": row["idFeriado"],
                    "fecha": fecha_str,
                    "nombre": row["nombre"],
                    "tipo": row["tipo"],
                    "es_medio_dia": row["es_medio_dia"],
                    "_saveStatus": "saved"
                }
                feriados.append(feriado)
            return feriados

        except Exception as ex:
            return {"error": f"No se pudo obtener feriados en servicio: {str(ex)}"}
        
    @staticmethod
    def get_feriados_formateados_service(db):
        try:
            data = FeriadoRepository.getFeriados(db)
            feriados = []
            for row in data:
                fecha_str = row["fecha"].strftime("%Y-%m-%d")
                fecha_formateada = fecha_str[5:]
                feriado = {
                    "idFeriado": row["idFeriado"],
                    "fecha": fecha_formateada,
                    "nombre": row["nombre"],
                    "tipo": row["tipo"],
                    "es_medio_dia": row["es_medio_dia"],
                }
                feriados.append(feriado)
            return feriados

        except Exception as ex:
            return {"error": f"No se pudo obtener feriados en servicio: {str(ex)}"}
    
    @staticmethod
    def get_fechas_de_feriados_formateados_service(db):
        try:
            data = FeriadoRepository.getFeriados_dia_completo(db)
            
            return [
                row["fecha"].strftime("%m-%d")
                for row in data
                if row["fecha"] is not None
            ]

        except Exception as ex:
            return {"error": f"No se pudo obtener feriados en servicio: {str(ex)}"}
    
    @staticmethod
    def getFeriados_medio_dia_formateados_service(db):
        try:
            data = FeriadoRepository.getFeriados_medio_dia(db)
            
            return [
                row["fecha"].strftime("%m-%d")
                for row in data
                if row["fecha"] is not None
            ]

        except Exception as ex:
            return {"error": f"No se pudo obtener feriados en servicio: {str(ex)}"}
    
    @staticmethod
    def getFeriadoById_service(db, idFeriado):
        try:
            data = FeriadoRepository.getFeriadoById(db, idFeriado)
            feriado = {
                "idFeriado": data["idFeriado"],
                "fecha": data["fecha"],
                "nombre": data["nombre"],
                "tipo": data["tipo"],
                "es_medio_dia": data["es_medio_dia"],
            }
            
            return feriado

        except Exception as ex:
            return {"error": f"No se pudo obtener feriados en servicio: {str(ex)}"}
            
    @staticmethod
    def createFeriado_service(db, data):
        try:
            fecha = data.get("fecha")
            nombre = data.get("nombre")
            tipo = data.get("tipo")
            es_medio_dia = data.get("es_medio_dia")
            
            required_fields = {
                "fecha": fecha, 
                "nombre": nombre, 
                "tipo": tipo, 
                "es_medio_dia": es_medio_dia, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            resultado = FeriadoRepository.createFeriado(db, fecha, nombre, tipo, es_medio_dia)

            if resultado.get("success"):
                Feriado_Service.refrescar_cache_feriados(db)

            return resultado
        
        except Exception as ex:
            return {"error": f"No se pudo crear la línea en el servicio. {str(ex)}"}
        
    @staticmethod
    def updateFeriado_service(db, data):
        try:
            idFeriado = data.get("idFeriado")
            fecha = data.get("fecha")
            nombre = data.get("nombre")
            tipo = data.get("tipo")
            es_medio_dia = data.get("es_medio_dia")

            required_fields = {
                    "idFeriado": idFeriado, 
                    "fecha": fecha, 
                    "nombre": nombre, 
                    "tipo": tipo, 
                    "es_medio_dia": es_medio_dia, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            resultado = FeriadoRepository.updateFeriado(db, idFeriado, fecha, nombre, tipo, es_medio_dia)

            if resultado.get("success"):
                Feriado_Service.refrescar_cache_feriados(db)

            return resultado
        
        except Exception as ex:
            return {"error": f"No se pudo modificar la línea. {str(ex)}"}
        
    @staticmethod
    def deleteFeriado_service(db, data):
        try:
            idFeriado = data.get("idFeriado")
            
            if not idFeriado:
                return {"error": "ID de la línea es requerido."}
            
            resultado = FeriadoRepository.deleteFeriado(db, idFeriado)

            if resultado.get("success"):
                Feriado_Service.refrescar_cache_feriados(db)

            return resultado
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la línea. {ex}"}
        
    @staticmethod
    def refrescar_cache_feriados(db):
        current_app.config["FERIADOS_GT"] = set(
            Feriado_Service.get_fechas_de_feriados_formateados_service(db)
        )
        current_app.config["FERIADOS_MEDIO_DIA"] = set(
            Feriado_Service.getFeriados_medio_dia_formateados_service(db)
        )