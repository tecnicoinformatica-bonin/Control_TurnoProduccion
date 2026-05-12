from app.extensions.slugify import Slugify

class Usuario_Permiso_Repository:
    @staticmethod
    def getUsuario_Permisos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_usuario_permiso
            """
            cursor.execute(query)

            usuario_permisos = cursor.fetchall()

            return usuario_permisos
        
        except Exception as ex:
            return {"error": f"No se pueden listar los usuario_permisos en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createUsuario_Permiso(db, idUsuario, idPermiso):
        cursor = None

        try:
            data = Usuario_Permiso_Repository.getUsuario_Permisos(db)
            idUsuario = int(idUsuario)
            idPermiso = int(idPermiso)

            exists = any(
                int(row[0]) == idUsuario and int(row[1]) == idPermiso
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario ya tiene ese permiso."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_usuario_permiso(idUsuario, idPermiso)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idUsuario, idPermiso,))
            
            db.connection.commit()

            newUsuario_Permiso = {
                "idUsuario": idUsuario, 
                "idPermiso": idPermiso,          
            }

            return {"mensaje": f"Usuario_Permiso creado correctamente. ID: {newUsuario_Permiso['idUsuario']}, Rol: {newUsuario_Permiso['idPermiso']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear usuario_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateUsuario_Permiso(db, idUsuario, idPermiso):
        cursor = None

        try: 
            data = Usuario_Permiso_Repository.getUsuario_Permisos(db)
            idUsuario = int(idUsuario)
            idPermiso = int(idPermiso)

            exists = any(
                int(row[0]) == idUsuario and int(row[1]) == idPermiso
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario {idUsuario} ya tiene ese permiso."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario_permiso SET idPermiso = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (idPermiso, idUsuario))
            
            db.connection.commit()

            editedUsuario_Permiso = {
                "idUsuario": idUsuario, 
                "idPermiso": idPermiso, 
            }

            return {"mensaje": f"Usuario_Permiso_ modificado correctamente. ID: {editedUsuario_Permiso['idUsuario']}, Rol: {editedUsuario_Permiso['idPermiso']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar usuario_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteUsuario_Permiso(db, idUsuario, idPermiso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_usuario_permiso
            WHERE idUsuario = %s AND idPermiso = %s
            """

            cursor.execute(query, (idUsuario, idPermiso, ))
            db.connection.commit()
            
            return {"mensaje": "Usuario_Permiso eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar usuario_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()