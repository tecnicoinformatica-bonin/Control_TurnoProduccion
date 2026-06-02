import MySQLdb

from app.extensions.slugify import Slugify

class Motivo_desasignacionRepository:
    @staticmethod
    def getMotivo_desasignacionById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_motivo_desasignacion
            WHERE idMotivo = %s
            """

            cursor.execute(query, (id,))
            motivo_desasignacion = cursor.fetchone()

            return motivo_desasignacion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener motivo_desasignacion. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getMotivos_desasignacion(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_motivo_desasignacion
            ORDER BY descripcion
            """
            cursor.execute(query)

            motivos_desasignacion = cursor.fetchall()

            return motivos_desasignacion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener lista de motivo_desasignacion. {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    

    @staticmethod
    def createMotivo_desasignacion(db, descripcion):
        cursor = None

        try:
            data = Motivo_desasignacionRepository.getMotivos_desasignacion(db)
            slugDescripcion = Slugify.slugify(descripcion)

            exists = any(
                Slugify.slugify(row["descripcion"]) == slugDescripcion
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un motivo con esa descripción: {descripcion}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_motivo_desasignacion(descripcion)
                VALUES (%s)
                """
            cursor.execute(query, (descripcion,))
            
            db.connection.commit()

            newMotivo_desasignacion = {
                "idMotivo": cursor.lastrowid, 
                "descripcion": descripcion,
            }

            return newMotivo_desasignacion

        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo crear motivo_desasignacion en repositorio: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateMotivo_desasignacion(db, idMotivo, descripcion):
        cursor = None

        try: 
            data = Motivo_desasignacionRepository.getMotivos_desasignacion(db)
            slugDescripcion = Slugify.slugify(descripcion)
            
            exists = any(
                int(row["idMotivo"]) != int(idMotivo)
                and Slugify.slugify(row["descripcion"]) == slugDescripcion
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un motivo con esa descripción: {descripcion}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_motivo_desasignacion SET descripcion = %s
                WHERE idMotivo = %s
                """
            
            cursor.execute(query, (descripcion, idMotivo,))
            
            db.connection.commit()

            editedMotivo_desasignacion = {
                "idMotivo": idMotivo,
                "descripcion": descripcion,
            }

            return editedMotivo_desasignacion

        except Exception as ex:
            db.connection.rollback()                        
            raise Exception (f"No se pudo modificar motivo_desasignacion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteMotivo_desasignacion(db, idMotivo):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_motivo_desasignacion
            WHERE idMotivo = %s
            """

            cursor.execute(query, (idMotivo,))
            db.connection.commit()
            
            return {"mensaje": "Motivo_desasignacion eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar motivo_desasignacion en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()