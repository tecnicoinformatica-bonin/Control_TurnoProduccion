from app.api.rol_permiso.rol_permiso_repository import Rol_Permiso_Repository

class Rol_Permiso_Service():
    @staticmethod
    def getRol_Permisos_service(db):
        try:
            data = Rol_Permiso_Repository.getRol_Permisos(db)
            rol_permisos = []
            for row in data:
                rol_permiso = {
                    "idRol": row["idRol"], 
                    "idPermiso": row["idPermiso"], 
                }
                rol_permisos.append(rol_permiso)
            return rol_permisos

        except Exception as ex:
            return {"error": f"No se pudo obtener rol_permisos. {str(ex)}"}
    
    @staticmethod
    def getPermisosByRol_service(db, idRol):
        try:
            data = Rol_Permiso_Repository.getPermisosByRol(db, idRol)
            rol_permisos = []
            for row in data:
                rol_permiso = {
                    "idRol": row[0],
                    "idPermiso": row[1],
                }
                rol_permisos.append(rol_permiso)
            return rol_permisos

        except Exception as ex:
            return {"error": f"No se pudo obtener rol_permisos. {str(ex)}"}
            
    @staticmethod
    def createRol_Permiso_service(db, data):
        try:
            idRol = data.get("idRol")
            idPermiso = data.get("idPermiso")
            
            required_fields = {
                    "idRol": idRol, 
                    "idPermiso": idPermiso, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Rol_Permiso_Repository.createRol_Permiso(db, idRol, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el rol_permiso. {ex}"}


    @staticmethod
    def create_rol_permiso_con_duplicados_service(db, idRol, idPermiso):
        try:            
            required_fields = {
                    "idRol": idRol, 
                    "idPermiso": idPermiso, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Rol_Permiso_Repository.create_rol_permiso_con_duplicados(db, idRol, idPermiso)
        
        except Exception as ex:
            raise Exception (f"No se pudo crear el rol_permiso. {str(ex)}")
        
    @staticmethod
    def updateRol_Permiso_service(db, data):
        try:
            idRol = data.get("idRol")
            idPermiso = data.get("idPermiso")
            
            required_fields = {
                    "idRol": idRol, 
                    "idPermiso": idPermiso, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Rol_Permiso_Repository.updateRol_Permiso(db, idRol, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el rol_permiso. {ex}"}
        
    @staticmethod
    def deleteRol_Permiso_service(db, data):
        try:
            idRol = data.get("idRol")
            idPermiso = data.get("idPermiso")
            
            if not idRol or not idPermiso:
                return {"error": "ID de roll e ID de permiso de la rol_permiso son requeridos."}
            
            return Rol_Permiso_Repository.deleteRol_Permiso(db, idRol, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la rol_permiso. {ex}"}

    @staticmethod
    def exists_rol_permiso(db, idRol, idPermiso):
        try:
            rol_permisos = Rol_Permiso_Repository.getRol_Permisos(db)

            avaliable = any(
                int(idRol) == int(rp["idRol"])
                and int(idPermiso) == int(rp["idPermiso"])
                for rp in rol_permisos
            )

            return {
                "available": not avaliable
            }

        except Exception as ex:
            raise Exception(f"No se pudo validar en el servicio: {str(ex)}")