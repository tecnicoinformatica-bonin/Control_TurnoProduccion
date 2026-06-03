from datetime import datetime

import pytz

from app.api.importacion.importacion_repository import ImportacionRepository
from app.extensions.slugify import Slugify

class Importacion_Service():
    @staticmethod
    def getImportaciones_service(db):
        try:
            data = ImportacionRepository.getImportaciones(db)
            importaciones = []
            for row in data:
                importacion = {
                    "idImportacion": row["idImportacion"],
                    "nombre_archivo": row["nombre_archivo"],
                    "fecha_inicio": row["fecha_inicio"],
                    "fecha_fin": row["fecha_fin"],
                    "registros": row["registros"],
                    "idUsuario": row["idUsuario"],
                    "fecha_creacion": row["fecha_creacion"]
                }
                importaciones.append(importacion)
            return importaciones

        except Exception as ex:
            return {
                "success": False,
                "error": f"No se pudo obtener líneas en servicio: {str(ex)}"
            }
    
    @staticmethod
    def getImportacionById_service(db, idImportacion):
        try:
            data = ImportacionRepository.getImportacionById(db, idImportacion)
            importacion = {
                "idImportacion": data["idImportacion"],
                "nombre_archivo": data["nombre_archivo"],
                "fecha_inicio": data["fecha_inicio"],
                "fecha_fin": data["fecha_fin"],
                "registros": data["registros"],
                "idUsuario": data["idUsuario"],
                "fecha_creacion": data["fecha_creacion"]
            }
            
            return importacion

        except Exception as ex:
            return {
                "succes": False,
                "error": f"No se pudo obtener líneas en servicio: {str(ex)}"
            }
            
    @staticmethod
    def createImportacion_service(db, data):
        try:
            nombre_archivo = data.get("nombre_archivo")
            idUsuario = data.get("idUsuario")
            
            required_fields = {
                    "nombre_archivo": nombre_archivo, 
                    "idUsuario": idUsuario, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            # Timezone de Guatemala
            tz = pytz.timezone("America/Guatemala")

            # Hora actual REAL 
            fecha_inicio = datetime.now(tz)
            
            return ImportacionRepository.createImportacion(db, nombre_archivo, fecha_inicio, idUsuario)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la importación. {str(ex)}"}
   
    @staticmethod
    def cerrarImportacion_service(db, idImportacion, registros):
        try:
            # Timezone de Guatemala
            tz = pytz.timezone("America/Guatemala")

            # Hora actual REAL 
            fecha_fin = datetime.now(tz)
            
            return ImportacionRepository.cerrarImportacion(db, idImportacion, fecha_fin, registros)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la importación. {ex}"}