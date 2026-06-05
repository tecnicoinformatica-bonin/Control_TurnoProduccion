from datetime import datetime, timedelta
import MySQLdb
import pytz

class ProgramacionRepository:
    @staticmethod
    def getProgramacionById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_programacion
            WHERE idProgramacion = %s
            """

            cursor.execute(query, (id,))
            programacion = cursor.fetchone()

            return programacion
        
        except Exception as ex:
            return {"error": f"No se pudo obtener la programación por ID en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCountsByLine(db, idProgramacion, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                T1.idLinea,
                T1.nameLinea,
                COUNT(T0.idLinea) AS total_linea,
                T1.minimo_requerido,
                T1.minimo_requerido - COUNT(T0.idLinea) AS diferencia
            FROM turnos_linea AS T1
            LEFT JOIN turnos_registro AS T0
                ON T1.idLinea = T0.idLinea
                AND T0.idProgramacion = %s
            WHERE T1.idDepartment = %s
            GROUP BY 
                T1.idLinea,
                T1.nameLinea,
                T1.minimo_requerido
            """

            cursor.execute(query, (idProgramacion, idDepartment,))
            detalles_total = cursor.fetchall()

            return detalles_total
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el conteo ID programación en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getProgramacionByDate(db, fecha):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_programacion
            WHERE fecha = %s
            """

            cursor.execute(query, (fecha,))
            programacion = cursor.fetchone()

            return programacion
        
        except Exception as ex:
            return {"error": f"No se pudo obtener la programación por fecha en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getProgramacionByDateAndIdDepartment(db, fecha, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_programacion
            WHERE fecha = %s AND idDepartment = %s
            """

            cursor.execute(query, (fecha,idDepartment,))
            programacion = cursor.fetchone()

            return programacion
        
        except Exception as ex:
            return {"error": f"No se pudo obtener la programación por fecha y ID Departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getProgramaciones(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_programacion
            """
            cursor.execute(query)

            programaciones = cursor.fetchall()

            return programaciones
        
        except Exception as ex:
            return {"error": f"No se pudo obtener las programaciones en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getProgramacionesActivas(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_programacion
            WHERE estado = 'BORRADOR' OR estado = 'VERIFICADO'
            """
            cursor.execute(query)

            programaciones = cursor.fetchall()

            return programaciones
        
        except Exception as ex:
            return {"error": f"No se pudo obtener las programaciones en borrador, en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getProgramacionesCerradas(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_programacion
            WHERE estado = 'CERRADO'
            """
            cursor.execute(query)

            programaciones = cursor.fetchall()

            return programaciones
        
        except Exception as ex:
            return {"error": f"No se pudo obtener las programaciones en borrador, en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getProgramacionesActivasByIdDepartment(db, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_programacion
            WHERE estado in ('BORRADOR', 'VERIFICADO')
            AND idDepartment = %s
            """
            cursor.execute(query, (idDepartment,))

            programaciones = cursor.fetchall()

            return programaciones
        
        except Exception as ex:
            return {"error": f"No se pudo obtener las programaciones en borrador, en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getProgramacionesCerradasByIdDepartment(db, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_programacion
            WHERE estado = 'CERRADO'
            AND idDepartment = %s
            """
            cursor.execute(query, (idDepartment,))

            programaciones = cursor.fetchall()

            return programaciones
        
        except Exception as ex:
            return {"error": f"No se pudo obtener las programaciones en borrador, en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createProgramacion(db, fecha, idDepartment, elaborado_por, fecha_creacion, estado):
        cursor = None

        try: 
            if(ProgramacionRepository.getProgramacionByDateAndIdDepartment(db, fecha, idDepartment)):
                return {"error": "ID del programacion de esa fecha ya existe para ese departamento."}

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_programacion(fecha, idDepartment, elaborado_por, fecha_creacion, estado)
                VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(query, (fecha, idDepartment, elaborado_por, fecha_creacion, estado,))
            
            db.connection.commit()

            newProgramacion = {
                "idProgramacion": cursor.lastrowid,
                "fecha": fecha, 
                "idDepartment": idDepartment, 
                "elaborado_por": elaborado_por, 
                "estado": estado,        
                "fecha_creacion": fecha_creacion,        
            }

            return newProgramacion["idProgramacion"]
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo crear la programación por ID en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def cerrarProgramacion(db, idProgramacion, elaborado_por, estado, fecha_cierre, cerrado_por):
        cursor = None

        try: 
            # if(ProgramacionRepository.getProgramacionById(db, idProgramacion)):
            #     return {"error": "ID del programacion de esa fecha ya existe para ese departamento."}

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_programacion SET elaborado_por = %s, estado = %s, fecha_cierre = %s, cerrado_por = %s
                WHERE idProgramacion = %s
                """
            cursor.execute(query, (elaborado_por, estado, fecha_cierre, cerrado_por, idProgramacion,))
            
            db.connection.commit()

            newProgramacion = {
                "idProgramacion": idProgramacion, 
                "elaborado_por": elaborado_por,  
                "estado": estado,  
                "fecha_cierre": fecha_cierre,  
                "cerrado_por": cerrado_por,  
            }

            return {"mensaje": f"Programacion cerrada correctamente. idProgramacion: {newProgramacion['idProgramacion']}, estado: {newProgramacion['estado']}"}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo cerrar la programación por ID en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def reOpenProgramacion(db, fecha, idDepartment, estado, fecha_reapertura, reabierto_por, motivo_reapertura):
        cursor = None

        try: 
            if estado == "CERRADO":
                return {"error": f"La programacion ya se encuentra cerrada."}
            
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_programacion SET estado = 'BORRADOR', fecha_reapertura = %s, reabierto_por = %s, motivo_reapertura = %s
                WHERE fecha = %s AND idDepartment = %s
                """
            
            cursor.execute(query, (fecha_reapertura, reabierto_por, motivo_reapertura, fecha, idDepartment,))
            
            db.connection.commit()

            editedProgramacion = {
                "fecha": fecha, 
                "idDepartment": idDepartment, 
                "estado": estado, 
                "fecha_reapertura": fecha_reapertura, 
                "reabierto_por": reabierto_por, 
                "motivo_reapertura": motivo_reapertura, 
            }

            return {"mensaje": f"Programacion modificada correctamente. Fecha: {editedProgramacion['fecha']}, ID del Departamento: {editedProgramacion['idDepartment']}, Estado: {editedProgramacion['estado']}"}

        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo cambiar el estado de la programación a BORRADOR en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_programacion
            WHERE idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            db.connection.commit()
            
            return {"mensaje": "Programacion eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar la programación por ID en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def cerrar_programaciones_vencidas(db):
        cursor = None

        try:
            cursor = db.connection.cursor()

            # Timezone de Guatemala
            tz = pytz.timezone("America/Guatemala")

            # Hora actual REAL 
            ahora = datetime.now(tz)

            query = """
            UPDATE turnos_programacion
            SET
                estado = 'CERRADO',
                fecha_cierre = %s,
                cerrado_por = 0
            WHERE 
                estado in ('BORRADOR', 'VERIFICADO')
                AND DATE_ADD(fecha, INTERVAL 1 DAY) + INTERVAL 15 HOUR <= %s
            """

            cursor.execute(query, (ahora, ahora))

            db.connection.commit()

            return cursor.rowcount

        except Exception as e:
            db.connection.rollback()
            raise Exception(f"Error cerrando programaciones: {str(e)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def confirmar_verificacion_programacion(db, idProgramacion, verificado_por):
        cursor = None

        try: 
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_programacion SET estado = 'VERIFICADO', verificado_por = %s
                WHERE idProgramacion = %s
                """
            cursor.execute(query, (verificado_por, idProgramacion,))
            
            db.connection.commit()

            programacion = {
                "idProgramacion": idProgramacion, 
                "verificado_por": verificado_por,  
            }

            return {
                "mensaje": f"Programación verificada correctamente. ID: {programacion['idProgramacion']}, verificado_por: {programacion['verificado_por']}",
                "programacion": programacion
            }
        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo verificar programación. {str(ex)}")

        finally:
            if cursor:
                cursor.close()