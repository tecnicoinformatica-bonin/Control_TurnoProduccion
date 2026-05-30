from app.api.empleado.empleado_repository import EmpleadoRepository
from app.extensions.slugify import Slugify

class Empleado_Service():
    @staticmethod
    def getEmpleadoById_service(db, id):
        try:
            data = EmpleadoRepository.getEmpleadoById(db, id)
            empleado = {
                "idEmpleado": data[0],
                "badgeNumber": data[1],
                "firstName": data[2],
                "secondName": data[3],
                "lastName": data[4],
                "lastName2": data[5],
                "position": data[6],
                "idDepartment": data[7],
                "activo": data[8],
                "idCentro": data[9],
                "idLinea": data[10],
                "idProceso": data[11],
            }
            
            return empleado

        except Exception as ex:
            return {"error": f"No se pudo obtener empleado en el servicio: {str(ex)}"}
        
    @staticmethod
    def getEmpleados_service(db):
        try:
            data = EmpleadoRepository.getEmpleados(db)
            empleados = []
            for row in data:
                empleado = {
                    "idEmpleado": row["idEmpleado"],
                    "badgeNumber": row["badgeNumber"],
                    "firstName": row["firstName"],
                    "secondName": row["secondName"],
                    "lastName": row["lastName"],
                    "lastName2": row["lastName2"],
                    "position": row["position"],
                    "idDepartment": row["idDepartment"],
                    "activo": row["activo"],
                    "idCentro": row["idCentro"],
                    "idLinea": row["idLinea"],
                    "idProceso": row["idProceso"],
                }
                empleados.append(empleado)
            return empleados

        except Exception as ex:
            return {"error": f"No se pudo obtener empleados en el servicio: {str(ex)}"}
    
    @staticmethod
    def getActiveEmpleadosByDepartment_service(db, idDeparment):
        try:
            data = EmpleadoRepository.getActiveEmpleadosByDepartment(db, idDeparment)
            empleados = []
            for row in data:
                empleado = {
                    "idEmpleado": row["idEmpleado"],
                    "badgeNumber": row["badgeNumber"],
                    "firstName": row["firstName"],
                    "secondName": row["secondName"],
                    "lastName": row["lastName"],
                    "lastName2": row["lastName2"],
                    "position": row["position"],
                    "idDepartment": row["idDepartment"],
                    "activo": row["activo"],
                    "idCentro": row["idCentro"],
                    "idLinea": row["idLinea"],
                    "idProceso": row["idProceso"],
                }
                empleados.append(empleado)
            return empleados

        except Exception as ex:
            return {"error": f"No se pudo obtener empleados activos en el servicio: {str(ex)}"}
            
    @staticmethod
    def createEmpleado_service(db, data):
        try:
            idEmpleado = data.get("idEmpleado")
            badgeNumber = data.get("badgeNumber")
            firstName = data.get("firstName")
            secondName = data.get("secondName")
            lastName = data.get("lastName")
            lastName2 = data.get("lastName2")
            position = data.get("position")
            idDepartment = data.get("idDepartment")
            activo = bool(data.get("activo"))
            idCentro = data.get("idCentro")
            idLinea = data.get("idLinea")
            idProceso = data.get("idProceso")

            required_fields = {
                    "idEmpleado": idEmpleado, 
                    "badgeNumber": badgeNumber, 
                    "firstName": firstName, 
                    "lastName": lastName, 
                    "position": position, 
                    "idDepartment": idDepartment,
                    "idCentro": idCentro,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return EmpleadoRepository.createEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, idLinea, idProceso)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el empleado en el servicio: {str(ex)}"}
        
    @staticmethod
    def updateEmpleado_service(db, data):
        try:
            oldIdEmpleado = data.get("oldIdEmpleado")
            oldBadgeNumber = data.get("oldBadgeNumber")
            idEmpleado = data.get("idEmpleado")
            badgeNumber = data.get("badgeNumber")
            firstName = data.get("firstName")
            secondName = data.get("secondName")
            lastName = data.get("lastName")
            lastName2 = data.get("lastName2")
            position = data.get("position")
            idDepartment = data.get("idDepartment")
            activo = bool(data.get("activo"))
            idCentro = data.get("idCentro")
            idLinea = data.get("idLinea")
            idProceso = data.get("idProceso")

            required_fields = {
                    "idEmpleado": idEmpleado, 
                    "badgeNumber": badgeNumber, 
                    "firstName": firstName, 
                    "lastName": lastName, 
                    "position": position, 
                    "idDepartment": idDepartment,
                    "oldIdEmpleado": oldIdEmpleado,
                    "oldBadgeNumber": oldBadgeNumber,
                    "idCentro": idCentro,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return EmpleadoRepository.updateEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, oldIdEmpleado, idLinea, idProceso, oldBadgeNumber)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el empleado en el servicio: {str(ex)}"}
        
    @staticmethod
    def deleteEmpleado_service(db, data):
        try:
            idEmpleado = data.get("idEmpleado")
            
            if not idEmpleado:
                return {"error": "ID del empleado es requerido."}
            
            return EmpleadoRepository.deleteEmpleado(db, idEmpleado)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el empleado en el servicio: {str(ex)}"}