import MySQLdb

from app.extensions.slugify import Slugify

class ImportacionRepository:
    @staticmethod
    def getImportacionById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_importacion_marcajes
            WHERE idImportacion = %s
            """

            cursor.execute(query, (id,))
            importacion = cursor.fetchone()

            return importacion
        
        except Exception as ex:
            raise Exception (f"No se puede encontrar en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    def getImportacionByName(db, nombre_archivo):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_importacion_marcajes
            WHERE nombre_archivo = %s
            """

            cursor.execute(query, (nombre_archivo,))
            importaciones = cursor.fetchone()

            return importaciones
        
        except Exception as ex:
            raise Exception(f"No se puede encontrar por nombre en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getImportaciones(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_importacion_marcajes
            ORDER BY nombre_archivo
            """
            cursor.execute(query)

            importaciones = cursor.fetchall()

            return importaciones
        
        except Exception as ex:
            raise Exception(f"No se puede encontrar por nombre en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createImportacion(db, nombre_archivo, fecha_inicio, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_importacion_marcajes(nombre_archivo, fecha_inicio, idUsuario)
                VALUES (%s, %s, %s)
                """
            cursor.execute(query, (nombre_archivo, fecha_inicio, idUsuario,))
            
            db.connection.commit()

            newImportacion = {
                "idImportacion": cursor.lastrowid, 
                "nombre_archivo": nombre_archivo,          
                "fecha_inicio": fecha_inicio,
                "idUsuario": idUsuario
            }

            return newImportacion["idImportacion"]
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception(f"No se pudo crear importacion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def cerrarImportacion(db, idImportacion, fecha_fin, registros):
        cursor = None

        try:
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_importacion_marcajes
                SET
                    fecha_fin = %s,
                    registros = %s
                WHERE idImportacion = %s
            """
            cursor.execute(query, (fecha_fin, registros, idImportacion,))
            
            db.connection.commit()

            updatedImportacion = {
                "idImportacion": idImportacion, 
                "fecha_fin": fecha_fin,
                "registros": registros
            }

            return updatedImportacion
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception(f"No se pudo crear importacion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()