from datetime import datetime

import MySQLdb
import pytz

class Registro_logRepository:
    @staticmethod
    def getRegistros_log(db):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_registro_log
            """

            cursor.execute(query, ())
            registro_logs = cursor.fetchall()

            return registro_logs
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idRegistro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRegistro_logById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_registro_log
            WHERE idLog = %s
            """

            cursor.execute(query, (id,))
            registro_log = cursor.fetchone()

            return registro_log
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el registro_log en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRegistros_logByRegistro(db, idRegistro):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_registro_log
            WHERE idRegistro = %s
            """

            cursor.execute(query, (idRegistro,))
            registro_logs = cursor.fetchall()

            return registro_logs
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idRegistro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistro_logByUsuario(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_registro_log
            WHERE idUsuario = %s
            """

            cursor.execute(query, (idUsuario,))
            registro_logs = cursor.fetchall()

            return registro_logs
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idUsuario en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistro_logByRegistroAndUsuario(db, idRegistro, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_registro_log
            WHERE idRegistro = %s AND idUsuario = %s
            """

            cursor.execute(query, (idRegistro, idUsuario,))
            registro_log = cursor.fetchone()

            return registro_log
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por Registro y Usuario en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def createRegistro_log(db, idRegistro, idUsuario, campo_modificado, valor_anterior, valor_nuevo):
        cursor = None

        try:
            cursor = db.connection.cursor()

            # Timezone de Guatemala
            tz = pytz.timezone("America/Guatemala")

            # Hora actual REAL 
            fecha_modificacion = datetime.now(tz)
            
            query = """
                INSERT INTO turnos_registro_log(idRegistro, idUsuario, fecha_modificacion, campo_modificado, valor_anterior, valor_nuevo)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (idRegistro, idUsuario, fecha_modificacion, campo_modificado, valor_anterior, valor_nuevo,))
            
            db.connection.commit()

            newLog = {
                "idLog": cursor.lastrowid,
                "idRegistro": idRegistro, 
                "idUsuario": idUsuario, 
                "fecha_modificacion": fecha_modificacion, 
                "campo_modificado": campo_modificado, 
                "valor_anterior": valor_anterior, 
                "valor_nuevo": valor_nuevo,
            }

            return newLog
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception (f"No se pudo crear registro_log_log en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    