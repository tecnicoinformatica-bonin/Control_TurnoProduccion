from app.api.permiso.permiso_repository import PermisoRepository
from app.extensions.slugify import Slugify

class Permiso_Service():
    @staticmethod
    def getPermisos_service(db):
        try:
            data = PermisoRepository.getPermisos(db)
            permisos = []
            for row in data:
                permiso = {
                    "idPermiso": row[0], 
                    "nombrePermiso": row[1], 
                    "descripcion": row[2], 
                }
                permisos.append(permiso)
            return permisos

        except Exception as ex:
            return {"error": f"No se pudo obtener líneas en servicio: {str(ex)}"}
    
    @staticmethod
    def getPermisoById_service(db, idPermiso):
        try:
            data = PermisoRepository.getPermisoById(db, idPermiso)
            permiso = {
                "idPermiso": data[0],
                "nombrePermiso": data[1],
                "descripcion": data[2],
            }
            
            return permiso

        except Exception as ex:
            return {"error": f"No se pudo obtener líneas en servicio: {str(ex)}"}
            
    @staticmethod
    def createPermiso_service(db, data):
        try:
            nombrePermiso = data.get("nombrePermiso")
            descripcion = data.get("descripcion")
            
            required_fields = {
                    "nombrePermiso": nombrePermiso, 
                    "descripcion": descripcion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return PermisoRepository.createPermiso(db, nombrePermiso, descripcion)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la línea. {ex}"}
        
    @staticmethod
    def updatePermiso_service(db, data):
        try:
            idPermiso = data.get("idPermiso")
            nombrePermiso = data.get("nombrePermiso")
            descripcion = data.get("descripcion")

            required_fields = {
                    "idPermiso": idPermiso, 
                    "nombrePermiso": nombrePermiso, 
                    "descripcion": descripcion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return PermisoRepository.updatePermiso(db, idPermiso, nombrePermiso, descripcion)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar la línea. {ex}"}
        
    @staticmethod
    def deletePermiso_service(db, data):
        try:
            idPermiso = data.get("idPermiso")
            
            if not idPermiso:
                return {"error": "ID de la línea es requerido."}
            
            return PermisoRepository.deletePermiso(db, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la línea. {ex}"}