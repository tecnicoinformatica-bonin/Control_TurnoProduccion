from app.api.linea.linea_repository import LineaRepository
from app.extensions.slugify import Slugify

class Linea_Service():
    @staticmethod
    def getLineas_service(db):
        try:
            data = LineaRepository.getLineas(db)
            lineas = []
            for row in data:
                linea = {
                    "idLinea": row[0], 
                    "nameLinea": row[1], 
                    "idDepartment": row[2], 
                }
                lineas.append(linea)
            return lineas

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createLinea_service(db, data):
        try:
            nameLinea = data.get("nameLinea")
            idDepartment = data.get("idDepartment")
            
            required_fields = {
                    "nameLinea": nameLinea, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return LineaRepository.createLinea(db, nameLinea, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la línea. {ex}"}
        
    @staticmethod
    def updateLinea_service(db, data):
        try:
            idLinea = data.get("idLinea")
            nameLinea = data.get("nameLinea")
            idDepartment = data.get("idDepartment")

            required_fields = {
                    "idLinea": idLinea, 
                    "nameLinea": nameLinea, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return LineaRepository.updateLinea(db, idLinea, nameLinea, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar la línea. {ex}"}
        
    @staticmethod
    def deleteLinea_service(db, data):
        try:
            idLinea = data.get("idLinea")
            
            if not idLinea:
                return {"error": "ID de la línea es requerido."}
            
            return LineaRepository.deleteLinea(db, idLinea)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la línea. {ex}"}