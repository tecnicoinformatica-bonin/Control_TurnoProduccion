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
                tmi.entrada_garita AS hora_entrada_garita,
                th.hora_fin AS hora_salida,
                tr.hora_fin AS hora_salida_digitada,
                tmi.salida_area AS hora_salida_marcaje,
                tmi.salida_garita  AS hora_salida_garita,
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
            AND te.idCentro NOT IN (1)
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
            usuario_autorizacion,
            idRegistro
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
                    usuario_autorizacion,
                    idRegistro
                )
                VALUES (
                    %s,
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
                    fecha_autorizacion = %s;
                """
            cursor.execute(query, (
                idEmpleado,
                fecha,
                horas_autorizadas,
                autorizado,
                observacion,
                fecha_autorizacion,
                usuario_autorizacion,
                idRegistro,
                fecha_autorizacion
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
                "idRegistro": idRegistro,
            }

            return newAutorizacion
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception(f"No se pudo crear autorizacion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    """ REPORTE """
    @staticmethod
    def get_detalles_autorizaciones_reporte(db, from_date, to_date, idDepartment):
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
                tr.badgeNumber,
                tr.idEmpleado,
                tr.idRegistro,
                tr.idCentro,
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
                tmi.entrada_garita AS hora_entrada_garita,
                th.hora_fin AS hora_salida,
                tr.hora_fin AS hora_salida_digitada,
                tmi.salida_area AS hora_salida_marcaje,
                tmi.salida_garita  AS hora_salida_garita,
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
            WHERE x.total_horas  > 0 AND NOT x.idCentro IN (1)
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
    def get_detalles_pendientes_reporte(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                x.*,
                x.total_horas - x.total_digitado AS diferencia,
                x.total_horas AS total_horas_autorizables,
                COALESCE(tah.autorizado, 0) AS autorizado
            FROM (SELECT
                tr.badgeNumber,
                tr.idRegistro,
                tr.idEmpleado,
                CONCAT_WS(' ',
                    te.firstName,
                    te.secondName,
                    te.lastName,
                    te.lastName2
                ) AS nombre_completo,
                tr.idCentro,
                tr.fecha,
                tr.diferencia_horas AS total_digitado,
                tmi.total_horas AS total_horas
            FROM turnos_registro tr
            INNER JOIN 
                turnos_empleado te
                ON te.idEmpleado = tr.idEmpleado
            INNER JOIN 
                turnos_marcaje_importado tmi
                ON tmi.idEmpleado = tr.idEmpleado AND tmi.fecha = tr.fecha
            WHERE 
                tr.fecha >= %s
                AND tr.fecha <= %s
                AND te.idDepartment = %s
            ) x
            LEFT JOIN turnos_autorizacion_horas tah
                ON tah.idEmpleado = x.idEmpleado
                AND tah.fecha = x.fecha
            WHERE 
                x.total_horas > 0 
                AND (x.total_horas - x.total_digitado) > 0
                AND NOT x.idCentro IN (1)
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
    def get_resumen_horas_autorizadas_reporte(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                x.*
            FROM(
                SELECT 
                tah.idEmpleado, 
                CONCAT_WS(' ',
                    te.firstName,
                    te.secondName,
                    te.lastName,
                    te.lastName2
                ) AS nombre_completo,
                SUM(tah.horas_autorizadas) AS suma_horas_autorizadas
            FROM turnos_autorizacion_horas tah 
            INNER JOIN 
                turnos_empleado te
                ON te.idEmpleado = tah.idEmpleado 
            WHERE 
                tah.fecha >= %s
                AND tah.fecha <= %s
                AND te.idDepartment = %s
                AND te.idCentro NOT IN (1)
            GROUP BY tah.idEmpleado 
            ORDER BY tah.idEmpleado
            ) x
            WHERE x.suma_horas_autorizadas > 0
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por empleado en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def get_horas_autorizadas_por_empleado_linea_fecha(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                tah.idEmpleado, 
                CONCAT_WS(' ',
                    te.firstName,
                    te.secondName,
                    te.lastName,
                    te.lastName2
                ) AS nombre_completo,
                tah.fecha,
                tcdc.nombreCentro,
                COALESCE(tl.nameLinea, tcdc.nombreCentro) AS nameLinea,
                tah.horas_autorizadas
            FROM turnos_autorizacion_horas tah 
            INNER JOIN 
                turnos_empleado te
                ON te.idEmpleado = tah.idEmpleado 
            INNER JOIN 
                turnos_registro tr
                ON tr.idRegistro = tah.idRegistro 
            INNER JOIN 
                turnos_centro_de_costo tcdc 
                ON tcdc.idCentro  = tr.idCentro
            LEFT JOIN 
                turnos_linea tl
                ON tl.idLinea = tr.idLinea 
            WHERE 
                tah.fecha >= %s
                AND tah.fecha <= %s
                AND te.idDepartment = %s
            ORDER BY tah.idEmpleado
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por empleado en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def get_horas_autorizadas_por_empleado_linea(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                tah.idEmpleado, 
                CONCAT_WS(' ',
                    te.firstName,
                    te.secondName,
                    te.lastName,
                    te.lastName2
                ) AS nombre_completo,
                tcdc.nombreCentro,
                COALESCE(tl.nameLinea, tcdc.nombreCentro) AS nameLinea,
                SUM(tah.horas_autorizadas) AS horas_autorizadas_linea
            FROM turnos_autorizacion_horas tah 
            INNER JOIN 
                turnos_empleado te
                ON te.idEmpleado = tah.idEmpleado 
            INNER JOIN 
                turnos_registro tr
                ON tr.idRegistro = tah.idRegistro 
            INNER JOIN 
                turnos_centro_de_costo tcdc 
                ON tcdc.idCentro  = tr.idCentro
            LEFT JOIN 
                turnos_linea tl
                ON tl.idLinea = tr.idLinea 
            WHERE 
                tah.fecha >= %s
                AND tah.fecha <= %s
                AND te.idDepartment = %s
            GROUP BY tah.idEmpleado, tcdc.nombreCentro, tl.nameLinea 
            ORDER BY tah.idEmpleado
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por empleado en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    # Primera parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_centros_de_costo(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT
                c.nombreCentro,
                COALESCE(cc.horas_autorizadas, 0) AS horas_centro_costo,
                COALESCE(li.horas_autorizadas, 0) AS horas_linea,
                COALESCE(cc.horas_autorizadas, 0)
                    - COALESCE(li.horas_autorizadas, 0) AS diferencia
            FROM turnos_centro_de_costo c
            LEFT JOIN (
                SELECT
                    tcdc.nombreCentro,
                    SUM(tah.horas_autorizadas) AS horas_autorizadas
                FROM turnos_autorizacion_horas tah
                INNER JOIN turnos_registro tr
                    ON tr.idRegistro = tah.idRegistro
                INNER JOIN turnos_centro_de_costo tcdc
                    ON tcdc.idCentro = tr.idCentro
                WHERE
                    tah.fecha >= %s
                    AND tah.fecha <= %s
                    AND tcdc.idDepartment = %s
                    AND tcdc.idCentro NOT IN (1)
                GROUP BY tcdc.nombreCentro
            ) cc
                ON cc.nombreCentro = c.nombreCentro
            LEFT JOIN (
                SELECT
                    COALESCE(
                        tl.nameLinea,
                        tcdc.nombreCentro
                    ) AS nombreLinea,
                    SUM(tah.horas_autorizadas) AS horas_autorizadas
                FROM turnos_autorizacion_horas tah
                INNER JOIN turnos_registro tr
                    ON tr.idRegistro = tah.idRegistro
                INNER JOIN turnos_centro_de_costo tcdc
                    ON tcdc.idCentro = tr.idCentro
                LEFT JOIN turnos_linea tl
                    ON tl.idLinea = tr.idLinea
                WHERE
                    tah.fecha >= %s
                    AND tah.fecha <= %s
                    AND tcdc.idDepartment = %s
                    AND tcdc.idCentro NOT IN (1)
                GROUP BY
                    COALESCE(
                        tl.nameLinea,
                        tcdc.nombreCentro
                    )
            ) li
                ON li.nombreLinea = c.nombreCentro
            WHERE
                c.idDepartment = %s
                AND c.idCentro NOT IN (1)
            ORDER BY c.nombreCentro;
            """
            cursor.execute(query, (from_date, to_date, idDepartment, from_date, to_date, idDepartment, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por centro de costo y línea en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    # Segunda parte parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_centros_asignados(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT
                tah.idRegistro,
                tcdc.nombreCentro,
                COALESCE(tl.nameLinea, tcdc.nombreCentro) AS nameLinea,
                SUM(tah.horas_autorizadas) as horas_autorizadas_linea
            FROM turnos_centro_de_costo tcdc 
            INNER JOIN 	
                turnos_registro tr
                ON tr.idCentro = tcdc.idCentro 
                AND tr.fecha >= %s AND tr.fecha <= %s
            LEFT JOIN 
                turnos_linea tl 
                ON tl.idLinea = tr.idLinea 
            INNER JOIN
                turnos_autorizacion_horas tah 
                ON tah.idRegistro = tr.idRegistro 
            WHERE 
                tcdc.idDepartment = %s
                AND tcdc.idCentro NOT IN (1)
            GROUP BY tah.idRegistro, tcdc.nombreCentro, tl.nameLinea
            ORDER BY tcdc.nombreCentro 
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por centro de costo en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    # Tercera parte parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_lineas_asignados(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT
                tah.idRegistro,
                COALESCE(tl.nameLinea, tcdc.nombreCentro) AS nameLinea,
                tcdc.nombreCentro,
                SUM(tah.horas_autorizadas) AS horas_autorizadas_centro
            FROM turnos_autorizacion_horas tah
            INNER JOIN turnos_registro tr
                ON tr.idRegistro = tah.idRegistro
            INNER JOIN turnos_centro_de_costo tcdc
                ON tcdc.idCentro = tr.idCentro
            LEFT JOIN turnos_linea tl
                ON tl.idLinea = tr.idLinea
            WHERE
                tah.fecha >= %s
                AND tah.fecha <= %s
                AND tcdc.idDepartment = %s
                AND (
                    tl.idLinea IS NULL
                    OR tl.idLinea NOT IN (9)
                )
            GROUP BY
                tah.idRegistro,
                COALESCE(tl.nameLinea, tcdc.nombreCentro),
                tcdc.nombreCentro
            ORDER BY
                tcdc.nombreCentro;
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por línea en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    # Cuarta parte parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_lineas(db, from_date, to_date, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
           SELECT
                COALESCE(tl.nameLinea, tcdc.nombreCentro) AS nameLinea,
                SUM(tah.horas_autorizadas) AS horas_autorizadas
            FROM turnos_autorizacion_horas tah
            INNER JOIN turnos_registro tr
                ON tr.idRegistro = tah.idRegistro
            INNER JOIN turnos_centro_de_costo tcdc
                ON tcdc.idCentro = tr.idCentro
            LEFT JOIN turnos_linea tl
                ON tl.idLinea = tr.idLinea
            WHERE
                tah.fecha >= %s
                AND tah.fecha <= %s
                AND tcdc.idDepartment = %s
                AND tr.idEmpleado NOT IN (120,662,921,1315,1429,1466,1477,2007)
            GROUP BY
                COALESCE(tl.nameLinea, tcdc.nombreCentro)
            ORDER BY
                COALESCE(tl.nameLinea, tcdc.nombreCentro);
            """
            cursor.execute(query, (from_date, to_date, idDepartment,))

            autorizaciones = cursor.fetchall()

            return autorizaciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar las horas autorizadas por centro de costo en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()