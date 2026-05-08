from app.api.empleado.empleado_repository import EmpleadoRepository
from app.extensions.slugify import Slugify

class Empleado_Service():
    @staticmethod
    def getEmpleadoById_service(db, id):
        try:
            data = EmpleadoRepository.getEmpleadoById(db, id)
            empleado = {
                "idEmpleado": data['idEmpleado'],
                "badgeNumber": data['badgeNumber'],
                "firstName": data['firstName'],
                "secondName": data['secondName'],
                "lastName": data['lastName'],
                "lastName2": data['lastName2'],
                "position": data['position'],
                "idDepartment": data['idDepartment'],
                "activo": data['activo'],
                "idCentro": data['idCentro'],
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
                    "idEmpleado": row[0], 
                    "badgeNumber": row[1], 
                    "firstName": row[2], 
                    "secondName": row[3], 
                    "lastName": row[4], 
                    "lastName2": row[5],
                    "position": row[6], 
                    "idDepartment": row[7],
                    "activo": row[8],
                    "idCentro": row[9],
                }
                empleados.append(empleado)
            return empleados

        except Exception as ex:
            return {"error": f"No se pudo obtener empleados en el servicio: {str(ex)}"}
    
    @staticmethod
    def getActiveEmpleados_service(db):
        try:
            data = EmpleadoRepository.getActiveEmpleados(db)
            empleados = []
            for row in data:
                empleado = {
                    "idEmpleado": row[0], 
                    "badgeNumber": row[1], 
                    "firstName": row[2], 
                    "secondName": row[3], 
                    "lastName": row[4], 
                    "lastName2": row[5],
                    "position": row[6], 
                    "idDepartment": row[7],
                    "activo": row[8],
                    "idCentro": row[8],
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
            
            return EmpleadoRepository.createEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro)
        
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
            
            return EmpleadoRepository.updateEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, oldIdEmpleado, oldBadgeNumber)
        
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