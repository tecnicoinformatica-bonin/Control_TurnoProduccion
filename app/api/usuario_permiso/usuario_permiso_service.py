from app.api.usuario_permiso.usuario_permiso_repository import Usuario_Permiso_Repository

class Usuario_Permiso_Service():
    @staticmethod
    def getUsuario_Permisos_service(db):
        try:
            data = Usuario_Permiso_Repository.getUsuario_Permisos(db)
            usuario_permisos = []
            for row in data:
                usuario_permiso = {
                    "idUsuario": row[0], 
                    "idPermiso": row[1], 
                }
                usuario_permisos.append(usuario_permiso)
            return usuario_permisos

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createUsuario_Permiso_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idPermiso = data.get("idPermiso")
            
            required_fields = {
                    "idUsuario": idUsuario, 
                    "idPermiso": idPermiso, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Permiso_Repository.createUsuario_Permiso(db, idUsuario, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el usuario_permiso. {ex}"}
        
    @staticmethod
    def updateUsuario_Permiso_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idPermiso = data.get("idPermiso")
            
            required_fields = {
                    "idUsuario": idUsuario, 
                    "idPermiso": idPermiso, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Permiso_Repository.updateUsuario_Permiso(db, idUsuario, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el usuario_permiso. {ex}"}
        
    @staticmethod
    def deleteUsuario_Permiso_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idPermiso = data.get("idPermiso")
            
            if not idUsuario or not idPermiso:
                return {"error": "ID de usuario e ID de rol de la usuario_permiso es requerido."}
            
            return Usuario_Permiso_Repository.deleteUsuario_Permiso(db, idUsuario, idPermiso)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la usuario_permiso. {ex}"}