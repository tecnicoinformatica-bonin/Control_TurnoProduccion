from app.api.motivo_desasignacion.motivo_desasignacion_repository import Motivo_desasignacionRepository
from app.extensions.slugify import Slugify

class Motivo_desasignacion_Service():
    @staticmethod
    def getMotivos_desasignacion_service(db):
        try:
            data = Motivo_desasignacionRepository.getMotivos_desasignacion(db)
            motivos_desasignacion = []
            for row in data:
                motivo_desasignacion = {
                    "idMotivo": row["idMotivo"],
                    "descripcion": row["descripcion"],
                }
                motivos_desasignacion.append(motivo_desasignacion)
            return motivos_desasignacion

        except Exception as ex:
            return {"error": f"No se pudo obtener motivos_desasignacion en servicio: {str(ex)}"}
    
    @staticmethod
    def getMotivo_desasignacionById_service(db, idMotivo):
        try:
            data = Motivo_desasignacionRepository.getMotivo_desasignacionById(db, idMotivo)
            motivo_desasignacion = {
                "idMotivo": data["idMotivo"], 
                "descripcion": data["descripcion"], 
            }
            
            return motivo_desasignacion

        except Exception as ex:
            return {"error": f"No se pudo obtener motivo_desasignacion en servicio: {str(ex)}"}
            
    @staticmethod
    def createMotivo_desasignacion_service(db, data):
        try:
            descripcion = data.get("descripcion")
            
            required_fields = {
                "descripcion": descripcion, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return {
                "mensaje": "Creado exitosamente",
                "Creado": Motivo_desasignacionRepository.createMotivo_desasignacion(db, descripcion)
                }
        
        except Exception as ex:
            return {"error": f"No se pudo crear el motivo_desasignacion en el servicio. {str(ex)}"}
        
    @staticmethod
    def updateMotivo_desasignacion_service(db, data):
        try:
            idMotivo = data.get("idMotivo")
            descripcion = data.get("descripcion")

            required_fields = {
                    "idMotivo": idMotivo, 
                    "descripcion": descripcion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return {
                "mensaje": "Modificado exitosamente",
                "Modificado": Motivo_desasignacionRepository.updateMotivo_desasignacion(db, idMotivo, descripcion)
            }
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el motivo_desasignacion. {str(ex)}"}
        
    @staticmethod
    def deleteMotivo_desasignacion_service(db, data):
        try:
            idMotivo = data.get("idMotivo")
            
            if not idMotivo:
                return {"error": "ID de la línea es requerido."}
            
            return Motivo_desasignacionRepository.deleteMotivo_desasignacion(db, idMotivo)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el motivo_desasignacion. {ex}"}