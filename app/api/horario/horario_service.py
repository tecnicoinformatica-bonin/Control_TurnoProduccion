from app.api.horario.horario_repository import HorarioRepository
from app.extensions.slugify import Slugify

class Horario_Service():
    @staticmethod
    def getHorarios_service(db):
        try:
            data = HorarioRepository.getHorarios(db)
            horarios = []
            for row in data:
                horario = {
                    "idHorario": row["idHorario"],
                    "descripcionHorario": row["descripcionHorario"],
                    "hora_inicio": row["hora_inicio"],
                    "hora_fin": row["hora_fin"],
                }
                horarios.append(horario)
            return horarios

        except Exception as ex:
            return {"error": f"No se pudo obtener horarios en servicio: {str(ex)}"}
    
    @staticmethod
    def getHorarioById_service(db, idHorario):
        try:
            data = HorarioRepository.getHorarioById(db, idHorario)
            horario = {
                "idHorario": data["idHorario"], 
                "descripcionHorario": data["descripcionHorario"], 
                "hora_inicio": data["hora_inicio"],
                "hora_fin": data["hora_fin"],
            }
            
            return horario

        except Exception as ex:
            return {"error": f"No se pudo obtener horario en servicio: {str(ex)}"}
            
    @staticmethod
    def createHorario_service(db, data):
        try:
            descripcionHorario = data.get("descripcionHorario")
            hora_inicio = data.get("hora_inicio")
            hora_fin = data.get("hora_fin")
            
            required_fields = {
                "descripcionHorario": descripcionHorario,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {
                    "success": False,
                    "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
                }

            result = HorarioRepository.createHorario(db, descripcionHorario, hora_inicio, hora_fin)

            if "error" in result:
                return result
            
            return {
                "success": True,
                "mensaje": "Creado exitosamente",
                "Creado": result
                }
        
        except Exception as ex:
            return {
                "error": f"No se pudo crear el horario en el servicio. {str(ex)}"
                }
        
    @staticmethod
    def updateHorario_service(db, data):
        try:
            idHorario = data.get("idHorario")
            descripcionHorario = data.get("descripcionHorario")
            hora_inicio = data.get("hora_inicio")

            hora_fin = data.get("hora_fin")
            required_fields = {
                "idHorario": idHorario, 
                "descripcionHorario": descripcionHorario, 
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {
                    "success": False,
                    "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
                }
            
            result = HorarioRepository.updateHorario(db, idHorario, descripcionHorario, hora_inicio, hora_fin)

            if "error" in result:
                return result
            
            return {
                "success": True,
                "mensaje": "Modificado exitosamente",
                "Modificado": result
            }
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el horario. {str(ex)}"}
        
    @staticmethod
    def deleteHorario_service(db, data):
        try:
            idHorario = data.get("idHorario")
            
            if not idHorario:
                return {
                    "success": False,
                    "error": "ID de la línea es requerido."
                }
            
            result = HorarioRepository.deleteHorario(db, idHorario)

            if "error" in result:
                return result
            
            return {
                "success": True,
                "mensaje": "Eliminado correctamente",
                "resutaldo": result
            }
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el horario. {ex}"}