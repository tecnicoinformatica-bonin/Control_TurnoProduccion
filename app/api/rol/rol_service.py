from app.api.rol.rol_repository import RolRepository

class Rol_Service():
    @staticmethod
    def getRoles_service(db):
        try:
            data = RolRepository.getRoles(db)
            roles = []
            for row in data:
                rol = {
                    "idRol": row[0], 
                    "nombre": row[1], 
                    "descripcion": row[2], 
                }
                roles.append(rol)
            return roles

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createRol_service(db, data):
        try:
            nombre = data.get("nombre")
            descripcion = data.get("descripcion")
            
            required_fields = {
                    "nombre": nombre, 
                    "descripcion": descripcion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return RolRepository.createRol(db, nombre, descripcion)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el rol. {ex}"}
        
    @staticmethod
    def updateRol_service(db, data):
        try:
            idRol = data.get("idRol")
            nombre = data.get("nombre")
            descripcion = data.get("descripcion")

            required_fields = {
                    "idRol": idRol, 
                    "nombre": nombre, 
                    "descripcion": descripcion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return RolRepository.updateRol(db, idRol, nombre, descripcion)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el rol. {ex}"}
        
    @staticmethod
    def deleteRol_service(db, data):
        try:
            idRol = data.get("idRol")
            
            if not idRol:
                return {"error": "ID del rol es requerido."}
            
            return RolRepository.deleteRol(db, idRol)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el rol. {ex}"}