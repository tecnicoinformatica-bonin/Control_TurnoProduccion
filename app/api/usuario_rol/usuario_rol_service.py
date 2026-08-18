from app.api.usuario_rol.usuario_rol_repository import Usuario_Rol_Repository

class Usuario_Rol_Service():
    @staticmethod
    def getUsuario_Roles_service(db):
        try:
            data = Usuario_Rol_Repository.getUsuario_Roles(db)
            usuario_roles = []
            for row in data:
                usuario_rol = {
                    "idUsuario": row["idUsuario"],
                    "idRol": row["idRol"],
                }
                usuario_roles.append(usuario_rol)
            return usuario_roles

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createUsuario_Rol_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idRol = data.get("idRol")
            
            required_fields = {
                    "idUsuario": idUsuario, 
                    "idRol": idRol, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Rol_Repository.createUsuario_Rol(db, idUsuario, idRol)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el usuario_rol. {ex}"}

    @staticmethod
    def create_usuario_rol_con_duplicados_service(db, idUsuario, idRol):
        try:
            required_fields = {
                "idUsuario": idUsuario, 
                "idRol": idRol, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Rol_Repository.create_usuario_rol_con_duplicados(db, idUsuario, idRol)
        
        except Exception as ex:
            raise Exception (f"No se pudo crear el usuario_rol. {str(ex)}")
        
    @staticmethod
    def updateUsuario_Rol_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idRol = data.get("idRol")
            
            required_fields = {
                    "idUsuario": idUsuario, 
                    "idRol": idRol, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Rol_Repository.updateUsuario_Rol(db, idUsuario, idRol)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el usuario_rol. {ex}"}
        
    @staticmethod
    def deleteUsuario_Rol_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idRol = data.get("idRol")
            
            if not idUsuario or not idRol:
                return {"error": "ID de usuario e ID de rol de la usuario_rol es requerido."}
            
            return Usuario_Rol_Repository.deleteUsuario_Rol(db, idUsuario, idRol)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la usuario_rol. {ex}"}

    @staticmethod
    def exists_usuario_rol(db, idUsuario, idRol):
        try:
            usuario_roles = Usuario_Rol_Repository.getUsuario_Roles(db)

            available = any(
                int(idUsuario) == ur["idUsuario"]
                and int(idRol) == ur["idRol"]
                for ur in usuario_roles
            )

            return {
                "available": not available
            }

        except Exception as ex:
            raise Exception(f"No se pudo realizar en servicio: {str(ex)}")