import MySQLdb

from app.extensions.slugify import Slugify

class HorarioRepository:
    @staticmethod
    def getHorarioById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_horario
            WHERE idHorario = %s
            """

            cursor.execute(query, (id,))
            horario = cursor.fetchone()

            return horario
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener horario. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getHorarios(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_horario
            ORDER BY descripcionHorario
            """
            cursor.execute(query)

            horarios = cursor.fetchall()

            return horarios
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener lista de horario. {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    

    @staticmethod
    def createHorario(db, descripcionHorario, hora_inicio, hora_fin):
        cursor = None

        try:
            data = HorarioRepository.getHorarios(db)
            slugDescripcion = Slugify.slugify(descripcionHorario)

            exists = any(
                Slugify.slugify(row["descripcionHorario"]) == slugDescripcion
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un horario con esa descripción: {descripcionHorario}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_horario(descripcionHorario, hora_inicio, hora_fin)
                VALUES (%s, %s, %s)
                """
            cursor.execute(query, (descripcionHorario, hora_inicio, hora_fin,))
            
            db.connection.commit()

            newHorario = {
                "idHorario": cursor.lastrowid, 
                "descripcionHorario": descripcionHorario,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }

            return newHorario

        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo crear horario en repositorio: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateHorario(db, idHorario, descripcionHorario, hora_inicio, hora_fin):
        cursor = None

        try: 
            data = HorarioRepository.getHorarios(db)
            slugDescripcion = Slugify.slugify(descripcionHorario)
            
            exists = any(
                int(row["idHorario"]) != int(idHorario)
                and Slugify.slugify(row["descripcionHorario"]) == slugDescripcion
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un horario con esa descripción: {descripcionHorario}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_horario SET descripcionHorario = %s, hora_inicio = %s, hora_fin = %s
                WHERE idHorario = %s
                """
            
            cursor.execute(query, (descripcionHorario, hora_inicio, hora_fin, idHorario,))
            
            db.connection.commit()

            editedHorario = {
                "idHorario": idHorario,
                "descripcionHorario": descripcionHorario,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }

            return editedHorario

        except Exception as ex:
            db.connection.rollback()                        
            raise Exception (f"No se pudo modificar horario en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteHorario(db, idHorario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_horario
            WHERE idHorario = %s
            """

            cursor.execute(query, (idHorario,))
            db.connection.commit()
            
            return {"mensaje": "Horario eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar horario en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()