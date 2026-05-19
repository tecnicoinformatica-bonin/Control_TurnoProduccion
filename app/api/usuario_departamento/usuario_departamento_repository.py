class Usuario_Departamento_Repository:
    @staticmethod
    def getUsuario_Departamentos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_usuario_departamento
            """
            cursor.execute(query)

            usuario_departamentos = cursor.fetchall()

            return usuario_departamentos
        
        except Exception as ex:
            return {"error": f"No se pueden listar los usuario_departamentos en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createUsuario_Departamento(db, idUsuario, idDepartment):
        cursor = None

        try:
            data = Usuario_Departamento_Repository.getUsuario_Departamentos(db)
            idUsuario = int(idUsuario)
            idDepartment = int(idDepartment)

            exists = any(
                int(row[0]) == idUsuario and int(row[1]) == idDepartment
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario ya puede ver ese departamento."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_usuario_departamento(idUsuario, idDepartment)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idUsuario, idDepartment,))
            
            db.connection.commit()

            newUsuario_Departamento = {
                "idUsuario": idUsuario, 
                "idDepartment": idDepartment,          
            }

            return {"mensaje": f"Usuario_Departamento creado correctamente. ID: {newUsuario_Departamento['idUsuario']}, Rol: {newUsuario_Departamento['idDepartment']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear usuario_departamento en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateUsuario_Departamento(db, idUsuario, idDepartment):
        cursor = None

        try: 
            data = Usuario_Departamento_Repository.getUsuario_Departamentos(db)
            idUsuario = int(idUsuario)
            idDepartment = int(idDepartment)

            exists = any(
                int(row[0]) == idUsuario and int(row[1]) == idDepartment
                for row in data
            )

            if exists:
                return {
                    "error": f"El usuario ya puede ver ese departamento."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario_departamento SET idDepartment = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (idDepartment, idUsuario))
            
            db.connection.commit()

            editedUsuario_Departamento = {
                "idUsuario": idUsuario, 
                "idDepartment": idDepartment, 
            }

            return {"mensaje": f"Usuario_Departamento_ modificado correctamente. ID: {editedUsuario_Departamento['idUsuario']}, Rol: {editedUsuario_Departamento['idDepartment']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar usuario_departamento en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteUsuario_Departamento(db, idUsuario, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_usuario_departamento
            WHERE idUsuario = %s AND idDepartment = %s
            """

            cursor.execute(query, (idUsuario, idDepartment, ))
            db.connection.commit()
            
            return {"mensaje": "Usuario_Departamento eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar usuario_departamento en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()