from app.api.departamento.departamento_repository import DepartamentoRepository
from app.extensions.slugify import Slugify

class Departamento_Service():
    @staticmethod
    def getDepartamentos_service(db):
        try:
            data = DepartamentoRepository.getDepartamentos(db)
            departments = []
            for row in data:
                department = {
                    "idDepartment": row[0],
                    "name": row[1],
                    "aplica_horas_extra" : row[2],
                    "nameSlug": Slugify.slugify(row[1])
                }
                departments.append(department)
            return departments

        except Exception as ex:
            return {"error": f"No se pudo obtener el departamento en el servicio: {str(ex)}"}
         
    @staticmethod
    def getDepartamentos_aplica_horas_extra_service(db):
        try:
            data = DepartamentoRepository.getDepartamentos_aplica_horas_extra(db)
            departamentos = []
            for row in data:
                departamento = {
                    "idDepartment": row[0],
                    "name": row[1],
                    "aplica_horas_extra" : row[2],
                    "nameSlug": Slugify.slugify(row[1])
                }
                departamentos.append(departamento)
            return departamentos

        except Exception as ex:
            return {"error": f"No se pudo obtener los departamentos en el servicio: {str(ex)}"}
        
    @staticmethod
    def createDepartamento_service(db, data):
        try:
            name = data.get("name")
            aplica_horas_extra = bool(data.get("aplica_horas_extra"))

            if not name:
                return {"error": "ID y Nombre del departamento son requeridos."}
            
            return DepartamentoRepository.createDepartamento(db, name, aplica_horas_extra)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el departamento en el servicio {str(ex)}"}
        
    @staticmethod
    def updateDepartamento_service(db, data):
        try:
            idDepartment = data.get("idDepartment")
            name = data.get("name")
            aplica_horas_extra = bool(data.get("aplica_horas_extra"))

            if not idDepartment or not name:
                return {"error": "ID y Nombre del departamento son requeridos."}
            
            return DepartamentoRepository.updateDepartamento(db, idDepartment, name, aplica_horas_extra)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el departamento en el servicio: {str(ex)}"}
        
    @staticmethod
    def deleteDepartamento_service(db, data):
        try:
            idDepartment = data.get("idDepartment")
            
            if not idDepartment:
                return {"error": "ID del departamento es requerido."}
            
            return DepartamentoRepository.deleteDepartamento(db, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el departamento en el servicio: {str(ex)}"}