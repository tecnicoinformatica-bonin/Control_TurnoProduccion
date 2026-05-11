from app.api.proceso.proceso_repository import ProcesoRepository

class Proceso_Service():
    @staticmethod
    def getProcesos_service(db):
        try:
            data = ProcesoRepository.getProcesos(db)
            procesos = []
            for row in data:
                proceso = {
                    "idProceso": row[0], 
                    "proceso": row[1], 
                    "idDepartment": row[2], 
                }
                procesos.append(proceso)
            return procesos

        except Exception as ex:
            return {"error": f"No se pudo obtener proceso en el servicio: {str(ex)}"}
   
    @staticmethod
    def getProcesoById_service(db, idProceso):
        try:
            data = ProcesoRepository.getProcesoById(db, idProceso)
            proceso = {
                "idProceso": data[0], 
                "proceso": data[1], 
                "idDepartment": data[2], 
            }

            return proceso

        except Exception as ex:
            return {"error": f"No se pudo obtener proceso en el servicio: {str(ex)}"}
            
    @staticmethod
    def createProceso_service(db, data):
        try:
            proceso = data.get("proceso")
            idDepartment = data.get("idDepartment")
            
            required_fields = {
                    "proceso": proceso, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProcesoRepository.createProceso(db, proceso, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el proceso. {ex}"}
        
    @staticmethod
    def updateProceso_service(db, data):
        try:
            idProceso = data.get("idProceso")
            proceso = data.get("proceso")
            idDepartment = data.get("idDepartment")

            required_fields = {
                    "idProceso": idProceso, 
                    "proceso": proceso, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProcesoRepository.updateProceso(db, idProceso, proceso, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el proceso. {ex}"}
        
    @staticmethod
    def deleteProceso_service(db, data):
        try:
            idProceso = data.get("idProceso")
            
            if not idProceso:
                return {"error": "ID del proceso es requerido."}
            
            return ProcesoRepository.deleteProceso(db, idProceso)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar le proceso. {ex}"}