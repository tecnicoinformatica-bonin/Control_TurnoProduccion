from app.extensions.slugify import Slugify

class Rol_Permiso_Repository:
    @staticmethod
    def getRol_Permisos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_rol_permiso
            """
            cursor.execute(query)

            rol_permisos = cursor.fetchall()

            return rol_permisos
        
        except Exception as ex:
            return {"error": f"No se pueden listar las rol_permisos en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getPermisosByRol(db, idRol):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_rol_permiso
            WHERE idRol = %s
            """
            cursor.execute(query, (idRol,))

            permisos = cursor.fetchall()

            return permisos
        
        except Exception as ex:
            return {"error": f"No se pueden listar las permisos por rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createRol_Permiso(db, idRol, idPermiso):
        cursor = None

        try:
            data = Rol_Permiso_Repository.getRol_Permisos(db)
            idRol = int(idRol)
            idPermiso = int(idPermiso)

            exists = any(
                row[0] == idRol and row[1] == idPermiso
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {idRol} ya tiene esa permiso asignada."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_rol_permiso(idRol, idPermiso)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idRol, idPermiso,))
            
            db.connection.commit()

            newRol_Permiso = {
                "idRol": idRol, 
                "idPermiso": idPermiso,          
            }

            return {"mensaje": f"Rol_Permiso_ creada correctamente. ID Rol: {newRol_Permiso['idRol']}, ID Permiso: {newRol_Permiso['idPermiso']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear rol_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateRol_Permiso(db, idRol, idPermiso):
        cursor = None

        try: 
            data = Rol_Permiso_Repository.getRol_Permisos(db)
            idRol = int(idRol)
            idPermiso = int(idPermiso)

            exists = any(
                row[0] == idRol and row[1] == idPermiso
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {idRol} ya tiene esa permiso asignada."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_rol_permiso SET idPermiso = %s
                WHERE idRol = %s
                """
            
            cursor.execute(query, (idPermiso, idRol))
            
            db.connection.commit()

            editedRol_Permiso = {
                "idRol": idRol, 
                "idPermiso": idPermiso, 
            }

            return {"mensaje": f"Rol_Permiso_ modificada correctamente. ID Rol: {editedRol_Permiso['idRol']}, ID Permiso: {editedRol_Permiso['idPermiso']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar rol_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteRol_Permiso(db, idRol, idPermiso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_rol_permiso
            WHERE idRol = %s AND idPermiso = %s
            """

            cursor.execute(query, (idRol, idPermiso, ))
            db.connection.commit()
            
            return {"mensaje": "Rol_Permiso eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar rol_permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()