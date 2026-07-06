import MySQLdb

from app.extensions.slugify import Slugify

class Registro_registro_motivo_desasignacionRepository:
    @staticmethod
    def get_count_motivos_desasignacion(db, from_date, to_date):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT 
                tmd.descripcion,
                COUNT(tmd.descripcion) AS conteo
            FROM turnos_registro_motivo_desasignacion trmd
            INNER JOIN 
                turnos_registro tr 
                ON tr.idRegistro = trmd.idRegistro 
            INNER JOIN 
                turnos_motivo_desasignacion tmd 
                ON tmd.idMotivo = trmd.idMotivo 
            WHERE 
                tr.fecha >= %s
                AND tr.fecha <= %s
            GROUP BY tmd.descripcion 
            ORDER BY tmd.descripcion  
            """

            cursor.execute(query, (from_date, to_date,))
            registro_motivo_desasignacion = cursor.fetchall()

            return registro_motivo_desasignacion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener detalles de motivos de desasignación. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def get_detalles_motivo_descripcion(db):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT trmd.idRegistro, trmd.idMotivo, tmd.descripcion, te.idEmpleado, te2.badgeNumber, CONCAT(te2.firstName, te2.lastName) AS NombreEmpleado
            FROM turnos_registro_motivo_desasignacion trmd 
            INNER JOIN 
                turnos_motivo_desasignacion tmd 
                ON trmd.idMotivo = tmd.idMotivo 
            LEFT JOIN 
                turnos_registro te 
                ON trmd.idRegistro = te.idRegistro 
            LEFT JOIN 
                turnos_empleado te2 
                ON te.idEmpleado = te2.idEmpleado 
            """

            cursor.execute(query)
            registro_motivo_desasignacion = cursor.fetchall()

            return registro_motivo_desasignacion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener detalles de motivos de desasignación. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def get_detalles_motivo_descripcion_by_idProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT trmd.idRegistro, trmd.idMotivo, tmd.descripcion, te.idEmpleado, te2.badgeNumber, CONCAT(te2.firstName, te2.lastName) AS NombreEmpleado
            FROM turnos_registro_motivo_desasignacion trmd 
            INNER JOIN 
                turnos_motivo_desasignacion tmd 
                ON trmd.idMotivo = tmd.idMotivo 
            LEFT JOIN 
                turnos_registro te 
                ON trmd.idRegistro = te.idRegistro 
            LEFT JOIN 
                turnos_empleado te2 
                ON te.idEmpleado = te2.idEmpleado 
            WHERE te.idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            registro_motivo_desasignacion = cursor.fetchall()

            return registro_motivo_desasignacion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener detalles de motivos de desasignación. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def create_registro_motivo_desasignacion(db, idRegistro, idMotivo):
        cursor = None

        try:
            data = Registro_registro_motivo_desasignacionRepository.get_detalles_motivo_descripcion(db)
            
            exists = any(
                int(row["idMotivo"]) == int(idMotivo)
                and int(row["idRegistro"]) == int(idRegistro)
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe ese registro."
                }
            
            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_registro_motivo_desasignacion(idRegistro, idMotivo)
                VALUES (%s, %s)
                """
            cursor.execute(query, (idRegistro, idMotivo,))
            
            db.connection.commit()

            newRegistro_motivo_desasignacion = {
                "idRegistro": idRegistro,
                "idMotivo": idMotivo, 
            }

            return newRegistro_motivo_desasignacion

        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo crear registro_motivo_desasignacion en repositorio: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()