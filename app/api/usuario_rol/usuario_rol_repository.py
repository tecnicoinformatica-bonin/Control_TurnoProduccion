from app.extensions.slugify import Slugify

class Usuario_Rol_Repository:
    @staticmethod
    def getUsuario_Roles(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_usuario_rol
            """
            cursor.execute(query)

            usuario_rols = cursor.fetchall()

            return usuario_rols
        
        except Exception as ex:
            return {"error": f"No se pueden listar los usuario_rols en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createUsuario_Rol(db, idUsuario, idRol):
        cursor = None

        try:
            data = Usuario_Rol_Repository.getUsuario_Roles(db)
            idUsuario = int(idUsuario)
            idRol = int(idRol)

            exists = any(
                row[0] == idUsuario and row[1] == idRol
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario {idUsuario} ya tiene ese rol."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_usuario_rol(idUsuario, idRol)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idUsuario, idRol,))
            
            db.connection.commit()

            newUsuario_Rol = {
                "idUsuario": idUsuario, 
                "idRol": idRol,          
            }

            return {"mensaje": f"Usuario_Rol_ creada correctamente. ID: {newUsuario_Rol['idUsuario']}, Rol: {newUsuario_Rol['idRol']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear usuario_rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateUsuario_Rol(db, idUsuario, idRol):
        cursor = None

        try: 
            data = Usuario_Rol_Repository.getUsuario_Roles(db)
            idUsuario = int(idUsuario)
            idRol = int(idRol)

            exists = any(
                row[0] == idUsuario and row[1] == idRol
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario {idUsuario} ya tiene ese rol."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario_rol SET idRol = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (idRol, idUsuario))
            
            db.connection.commit()

            editedUsuario_Rol = {
                "idUsuario": idUsuario, 
                "idRol": idRol, 
            }

            return {"mensaje": f"Usuario_Rol_ modificado correctamente. ID: {editedUsuario_Rol['idUsuario']}, Rol: {editedUsuario_Rol['idRol']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar usuario_rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteUsuario_Rol(db, idUsuario, idRol):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_usuario_rol
            WHERE idUsuario = %s AND idRol = %s
            """

            cursor.execute(query, (idUsuario, idRol, ))
            db.connection.commit()
            
            return {"mensaje": "Usuario_Rol eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar usuario_rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()