from app.api.importacion.importacion_repository import ImportacionRepository

class Importacion_Service():
    @staticmethod
    def getImportaciones_service(db):
        try:
            data = ImportacionRepository.getImportaciones(db)
            importaciones = []
            for row in data:
                fecha_inicio = row["fecha_inicio"].strftime("%d/%m/%Y %H:%M") if row["fecha_inicio"] is not None else None
                fecha_fin = row["fecha_fin"].strftime("%d/%m/%Y %H:%M") if row["fecha_fin"] is not None else None
                fecha_creacion = row["fecha_creacion"].strftime("%d/%m/%Y %H:%M") if row["fecha_creacion"] is not None else None
                importacion = {
                    "idImportacion": row["idImportacion"],
                    "nombre_archivo": row["nombre_archivo"],
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "registros": row["registros"],
                    "nombre_usuario": row["nombre_usuario"],
                    "fecha_creacion": fecha_creacion,
                }
                importaciones.append(importacion)
            return importaciones

        except Exception as ex:
            return {
                "success": False,
                "error": f"No se pudo realizar importación en servicio: {str(ex)}"
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
            fecha_inicio = data.get("fecha_inicio")
            
            required_fields = {
                    "nombre_archivo": nombre_archivo, 
                    "idUsuario": idUsuario, 
                    "fecha_inicio": fecha_inicio, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ImportacionRepository.createImportacion(db, nombre_archivo, fecha_inicio, idUsuario)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la importación. {str(ex)}"}
   
    @staticmethod
    def cerrarImportacion_service(db, idImportacion, fecha_fin, registros):
        try:
            return ImportacionRepository.cerrarImportacion(db, idImportacion, fecha_fin, registros)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la importación. {ex}"}