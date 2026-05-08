from app.extensions.slugify import Slugify

class RutaRepository:
    @staticmethod
    def getRutaById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_ruta
            WHERE idRuta = %s
            """

            cursor.execute(query, (id,))
            ruta = cursor.fetchone()

            return ruta
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el ruta en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    def getRutaByPath(db, path):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_ruta
            WHERE path = %s
            """

            cursor.execute(query, (path,))
            rutas = cursor.fetchall()

            return rutas
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por path en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRutas(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_ruta
            """
            cursor.execute(query)

            rutas = cursor.fetchall()

            return rutas
        
        except Exception as ex:
            return {"error": f"No se pueden listar los rutas en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
   
    @staticmethod
    def getRutasDESC(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_ruta
            ORDER BY path
            """
            cursor.execute(query)

            rutas = cursor.fetchall()

            return rutas
        
        except Exception as ex:
            return {"error": f"No se pueden listar los rutas de manera descendente en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createRuta(db, path):
        cursor = None

        try:
            data = RutaRepository.getRutas(db)
            slugRuta = Slugify.slugify(path)

            """  Row[2] is the descripcion an row[1] es el ruta """
            exists = any(
                Slugify.slugify(row[1]) == slugRuta
                for row in data
            )

            if exists:
                return {
                    "error": f"La ruta {path} ya existe."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_ruta(path)
                VALUES (%s)
                """
            cursor.execute(query, (path,))
            
            db.connection.commit()

            newRuta = {
                "idRuta": cursor.lastrowid, 
                "path": path,          
            }

            return {"mensaje": f"Ruta creada correctamente. ID: {newRuta['idRuta']}, Ruta: {newRuta['path']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateRuta(db, idRuta, path):
        cursor = None

        try: 
            data = RutaRepository.getRutas(db)
            slugRuta = Slugify.slugify(path)

            """  Row[2] is the descripcion an row[1] es el path """
            exists = any(
                Slugify.slugify(row[1]) == slugRuta
                for row in data
            )

            if exists:
                return {
                    "error": f"La ruta {path} ya existe"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_ruta SET path = %s
                WHERE idRuta = %s
                """
            
            cursor.execute(query, (path, idRuta))
            
            db.connection.commit()

            editedRuta = {
                "idRuta": idRuta, 
                "path": path, 
            }

            return {"mensaje": f"Ruta modificada correctamente. ID: {editedRuta['idRuta']}, Ruta: {editedRuta['path']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteRuta(db, idRuta):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_ruta
            WHERE idRuta = %s
            """

            cursor.execute(query, (idRuta,))
            db.connection.commit()
            
            return {"mensaje": "Ruta eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar ruta en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()