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
                    "minimo_requerido": row[3],
                }
                lineas.append(linea)
            return lineas

        except Exception as ex:
            return {"error": f"No se pudo obtener líneas en servicio: {str(ex)}"}
    
    @staticmethod
    def getLineasByDepartment_service(db, idDepartment):
        try:
            data = LineaRepository.getLineasByDepartment(db, idDepartment)
            lineas = []
            for row in data:
                linea = {
                    "idLinea": row["idLinea"],
                    "nameLinea": row["nameLinea"],
                    "idDepartment": row["idDepartment"],
                    "minimo_requerido": row["minimo_requerido"],
                }
                lineas.append(linea)
            return lineas

        except Exception as ex:
            return {"error": f"No se pudo obtener líneas en servicio: {str(ex)}"}
    
    @staticmethod
    def getLineaById_service(db, idLinea):
        try:
            data = LineaRepository.getLineaById(db, idLinea)
            linea = {
                "idLinea": data[0], 
                "nameLinea": data[1], 
                "idDepartment": data[2], 
                "minimo_requerido": data[3],
            }
            
            return linea

        except Exception as ex:
            return {"error": f"No se pudo obtener líneas en servicio: {str(ex)}"}
            
    @staticmethod
    def createLinea_service(db, data):
        try:
            nameLinea = data.get("nameLinea")
            idDepartment = data.get("idDepartment")
            minimo_requerido = data.get("minimo_requerido")
            
            required_fields = {
                "nameLinea": nameLinea, 
                "idDepartment": idDepartment, 
                "minimo_requerido": minimo_requerido, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return LineaRepository.createLinea(db, nameLinea, idDepartment, minimo_requerido)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la línea en el servicio. {str(ex)}"}
        
    @staticmethod
    def updateLinea_service(db, data):
        try:
            idLinea = data.get("idLinea")
            nameLinea = data.get("nameLinea")
            idDepartment = data.get("idDepartment")
            minimo_requerido = data.get("minimo_requerido")

            required_fields = {
                    "idLinea": idLinea, 
                    "nameLinea": nameLinea, 
                    "idDepartment": idDepartment, 
                    "minimo_requerido": minimo_requerido, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return LineaRepository.updateLinea(db, idLinea, nameLinea, idDepartment, minimo_requerido)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar la línea. {str(ex)}"}
        
    @staticmethod
    def deleteLinea_service(db, data):
        try:
            idLinea = data.get("idLinea")
            
            if not idLinea:
                return {"error": "ID de la línea es requerido."}
            
            return LineaRepository.deleteLinea(db, idLinea)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la línea. {ex}"}