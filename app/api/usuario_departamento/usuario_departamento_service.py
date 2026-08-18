from app.api.usuario_departamento.usuario_departamento_repository import Usuario_Departamento_Repository

class Usuario_Departamento_Service():
    @staticmethod
    def getUsuario_Departamentos_service(db):
        try:
            data = Usuario_Departamento_Repository.getUsuario_Departamentos(db)
            usuario_departamentos = []
            for row in data:
                usuario_departamento = {
                    "idUsuario": row["idUsuario"],
                    "idDepartment": row["idDepartment"],
                }
                usuario_departamentos.append(usuario_departamento)
            return usuario_departamentos

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createUsuario_Departamento_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idDepartment = data.get("idDepartment")
            
            required_fields = {
                "idUsuario": idUsuario, 
                "idDepartment": idDepartment, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Departamento_Repository.createUsuario_Departamento(db, idUsuario, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el usuario_departamento. {str(ex)}"}

    @staticmethod
    def create_usuario_departamento_con_duplicados_service(db, idUsuario, idDepartment):
        try:
            required_fields = {
                "idUsuario": idUsuario, 
                "idDepartment": idDepartment, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Departamento_Repository.create_usuario_departamento_con_duplicados(db, idUsuario, idDepartment)
        
        except Exception as ex:
            raise Exception(f"No se pudo crear el usuario_departamento. {str(ex)}")
        
    @staticmethod
    def updateUsuario_Departamento_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idDepartment = data.get("idDepartment")
            
            required_fields = {
                    "idUsuario": idUsuario, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Usuario_Departamento_Repository.updateUsuario_Departamento(db, idUsuario, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el usuario_departamento. {str(ex)}"}
        
    @staticmethod
    def deleteUsuario_Departamento_service(db, data):
        try:
            idUsuario = data.get("idUsuario")
            idDepartment = data.get("idDepartment")
            
            if not idUsuario or not idDepartment:
                return {"error": "ID de usuario e ID de rol de la usuario_departamento es requerido."}
            
            return Usuario_Departamento_Repository.deleteUsuario_Departamento(db, idUsuario, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la usuario_departamento. {str(ex)}"}

    @staticmethod
    def exists_usuario_departamento(db, idUsuario, idDepartment):
        try:
            usuario_departamentos = Usuario_Departamento_Repository.getUsuario_Departamentos(db, )

            available = any(
                int(idUsuario) == int(ud["idUsuario"])
                and int(idDepartment) == int(ud["idDepartment"])
                for ud in usuario_departamentos
            )

            return {
                "available": not available,
            }

        except Exception as ex: 
            raise Exception(f"No se pudo validar en servicio: {str(ex)}")