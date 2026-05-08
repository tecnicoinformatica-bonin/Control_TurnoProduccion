from app.extensions.slugify import Slugify

class Rol_Ruta_Repository:
    @staticmethod
    def getRol_Rutas(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_rol_ruta
            """
            cursor.execute(query)

            rol_rutas = cursor.fetchall()

            return rol_rutas
        
        except Exception as ex:
            return {"error": f"No se pueden listar las rol_rutas en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createRol_Ruta(db, idRol, idRuta):
        cursor = None

        try:
            data = Rol_Ruta_Repository.getRol_Rutas(db)
            idRol = int(idRol)
            idRuta = int(idRuta)

            exists = any(
                row[0] == idRol and row[1] == idRuta
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {idRol} ya tiene esa ruta asignada."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_rol_ruta(idRol, idRuta)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idRol, idRuta,))
            
            db.connection.commit()

            newRol_Ruta = {
                "idRol": idRol, 
                "idRuta": idRuta,          
            }

            return {"mensaje": f"Rol_Ruta_ creada correctamente. ID Rol: {newRol_Ruta['idRol']}, ID Ruta: {newRol_Ruta['idRuta']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear rol_ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateRol_Ruta(db, idRol, idRuta):
        cursor = None

        try: 
            data = Rol_Ruta_Repository.getRol_Rutas(db)
            idRol = int(idRol)
            idRuta = int(idRuta)

            exists = any(
                row[0] == idRol and row[1] == idRuta
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {idRol} ya tiene esa ruta asignada."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_rol_ruta SET idRuta = %s
                WHERE idRol = %s
                """
            
            cursor.execute(query, (idRuta, idRol))
            
            db.connection.commit()

            editedRol_Ruta = {
                "idRol": idRol, 
                "idRuta": idRuta, 
            }

            return {"mensaje": f"Rol_Ruta_ modificada correctamente. ID Rol: {editedRol_Ruta['idRol']}, ID Ruta: {editedRol_Ruta['idRuta']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar rol_ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteRol_Ruta(db, idRol, idRuta):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_rol_ruta
            WHERE idRol = %s AND idRuta = %s
            """

            cursor.execute(query, (idRol, idRuta, ))
            db.connection.commit()
            
            return {"mensaje": "Rol_Ruta eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar rol_ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()