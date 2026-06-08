import MySQLdb

from app.extensions.slugify import Slugify

class AutorizacionRepository:
    @staticmethod
    def getAutorizacionById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_autorizacion_horas
            WHERE idAutorizacion = %s
            """

            cursor.execute(query, (id,))
            autorizacion = cursor.fetchone()

            return autorizacion
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el Autorizacion en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAutorizacionByEmpleado(db, idEmpleado):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_autorizacion_horas
            WHERE idEmpleado = %s
            """

            cursor.execute(query, (idEmpleado,))
            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAutorizaciones(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_autorizacion_horas
            """
            cursor.execute(query)

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            return {"error": f"No se pueden listar los autorizaciones en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def get_detalles_autorizaciones(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                x.*,
                x.total_horas - total_digitado AS diferencia,
                x.total_horas AS total_horas_autorizables,    
                tah.horas_autorizadas,
                COALESCE(tah.autorizado, 0) AS autorizado,
                tah.observacion,
                tah.usuario_autorizacion,
                tah.fecha_autorizacion
            FROM (SELECT
                tr.idEmpleado,
                tr.idRegistro,
                CONCAT_WS(' ',
                    te.firstName,
                    te.secondName,
                    te.lastName,
                    te.lastName2
                ) AS nombre_completo,
                tr.fecha,
                th.hora_inicio AS hora_entrada,
                tr.hora_inicio AS hora_entrada_digitada,
                tmi.entrada_area  AS hora_entrada_marcaje,
                th.hora_fin AS hora_salida,
                tr.hora_fin AS hora_salida_digitada,
                tmi.salida_area AS hora_salida_marcaje,
                -- Llegó antes de la hora de entrada
                CASE
                    WHEN tr.hora_inicio < th.hora_inicio
                    THEN TIME_TO_SEC(
                        TIMEDIFF(th.hora_inicio, tr.hora_inicio)
                    ) / 3600
                    ELSE 0
                END AS horas_temprano,
                -- Salió después de la hora de salida
                CASE
                    WHEN tr.hora_fin > th.hora_fin
                    THEN TIME_TO_SEC(
                        TIMEDIFF(tr.hora_fin, th.hora_fin)
                    ) / 3600
                    ELSE 0
                END AS horas_tarde,
                tr.diferencia_horas AS total_digitado,
                tmi.total_horas AS total_horas
            FROM turnos_registro tr
            INNER JOIN turnos_empleado te
                ON te.idEmpleado = tr.idEmpleado
            INNER JOIN turnos_horario th
                ON th.idHorario = te.idHorario
            INNER JOIN turnos_marcaje_importado tmi
                ON tmi.idEmpleado = tr.idEmpleado AND tmi.fecha = tr.fecha
            WHERE tr.fecha >= %s
            AND tr.fecha <= %s
            AND te.idDepartment = %s
            ) x
            LEFT JOIN turnos_autorizacion_horas tah
                ON tah.idEmpleado = x.idEmpleado
                AND tah.fecha = x.fecha
            WHERE x.total_horas  > 0
            ORDER BY x.idEmpleado 
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar los autorizaciones en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    

    @staticmethod
    def guardar_autorizacion(
            db, 
            idEmpleado,
            fecha,
            horas_autorizadas,
            autorizado,
            observacion,
            fecha_autorizacion,
            usuario_autorizacion
        ):
        cursor = None

        try:
            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_autorizacion_horas (
                    idEmpleado,
                    fecha,
                    horas_autorizadas,
                    autorizado,
                    observacion,
                    fecha_autorizacion,
                    usuario_autorizacion
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ON DUPLICATE KEY UPDATE
                    horas_autorizadas = VALUES(horas_autorizadas),
                    autorizado = VALUES(autorizado),
                    observacion = VALUES(observacion),
                    usuario_autorizacion = VALUES(usuario_autorizacion),
                    fecha_autorizacion = NOW();
                """
            cursor.execute(query, (
                idEmpleado,
                fecha,
                horas_autorizadas,
                autorizado,
                observacion,
                fecha_autorizacion,
                usuario_autorizacion
            ))
            
            db.connection.commit()

            newAutorizacion = {
                "idAutorizacion": cursor.lastrowid, 
                "idEmpleado": idEmpleado,
                "fecha": fecha,
                "horas_autorizadas": horas_autorizadas,
                "autorizado": autorizado,
                "observacion": observacion,
                "fecha_autorizacion": fecha_autorizacion,
                "usuario_autorizacion": usuario_autorizacion,
            }

            return newAutorizacion
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception(f"No se pudo crear autorizacion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()