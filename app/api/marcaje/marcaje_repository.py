import MySQLdb

from app.extensions.slugify import Slugify
from app.extensions.db_boninsa import get_boninsa_connection

class MarcajeRepository:
    @staticmethod
    def get_marcajes_by_fecha(db, fecha):
        cursor: None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors)

            query = """
            SELECT * 
            FROM turnos_marcaje_importado
            WHERE fecha = %s
            """

            cursor.execute(query, (fecha,))

            result = cursor.fetchall()

            return result
        
        except Exception as ex:
            return Exception(f"No se pudo obtener marcajes de la fecha {fecha}. {str(ex)}")

    @staticmethod
    def get_summary_of_clocks(fecha):
        cursor = None

        try:
            db_boninsa = get_boninsa_connection()
            cursor = db_boninsa.cursor()

            query = """
             SELECT
                Dia as dia,
                Hora_Inicial as entrada_garita,
                Hora_Fin as salida_garita,
                Hora_IGSSini as entrada_area,
                Hora_IGSSfin as salida_area,
                Nombre as nombre_empleado,
                Codigo as idEmpleado, 
                horario as horario_inicio,
                Fecha as fecha,
                Horario_Fin as horario_fin,
                Area as area,
                Departamento as departamento
            FROM dbo.Horas_extraDep
            WHERE Fecha = ?
            ORDER BY Nombre
            """

            cursor.execute(query, (fecha,))

            columnas = [col[0] for col in cursor.description]

            resultado = [
                dict(zip(columnas, row))
                for row in cursor.fetchall()
            ]

            return resultado
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener datos de boninsa. {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createMarcaje(
        db, 
        idEmpleado,
        nombre_empleado,
        departamento,
        area,
        dia,
        fecha,
        entrada_garita,
        entrada_area,
        salida_area,
        salida_garita,
        hora_simple,
        hora_doble,
        total_horas,
        horario_inicio,
        horario_fin,
        fecha_importacion
    ):
        cursor = None

        try:
            cursor = db.connection.cursor()
            
            query = """
            INSERT INTO turnos_marcaje_importado(
                idEmpleado,
                nombre_empleado,
                departamento,
                area,
                dia,
                fecha,
                entrada_garita,
                entrada_area,
                salida_area,
                salida_garita,
                hora_simple,
                hora_doble,
                total_horas,
                horario_inicio,
                horario_fin,
                fecha_importacion
            )
            VALUES(
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,
                %s,%s, %s
            )
            ON DUPLICATE KEY UPDATE
                nombre_empleado = VALUES(nombre_empleado),
                departamento = VALUES(departamento),
                area = VALUES(area),
                entrada_garita = VALUES(entrada_garita),
                entrada_area = VALUES(entrada_area),
                salida_area = VALUES(salida_area),
                salida_garita = VALUES(salida_garita),
                hora_simple = VALUES(hora_simple),
                hora_doble = VALUES(hora_doble),
                total_horas = VALUES(total_horas),
                horario_inicio = VALUES(horario_inicio),
                horario_fin = VALUES(horario_fin),
                fecha_importacion = VALUES(fecha_importacion)
            """
            cursor.execute(query, (
                idEmpleado,
                nombre_empleado,
                departamento,
                area,
                dia,
                fecha,
                entrada_garita,
                entrada_area,
                salida_area,
                salida_garita,
                hora_simple,
                hora_doble,
                total_horas,
                horario_inicio,
                horario_fin,
                fecha_importacion,
            ))
            
            # db.connection.commit()

            newMarcaje = {
                "idMarcaje": cursor.lastrowid, 
                "idEmpleado": idEmpleado,
                "nombre_empleado": nombre_empleado,
                "departamento": departamento,
                "area": area,
                "dia": dia,
                "fecha": fecha,
                "entrada_garita": entrada_garita,
                "entrada_area": entrada_area,
                "salida_area": salida_area,
                "salida_garita": salida_garita,
                "hora_simple": hora_simple,
                "hora_doble": hora_doble,
                "total_horas": total_horas,
                "horario_inicio": horario_inicio,
                "horario_fin": horario_fin,
                "fecha_importacion": fecha_importacion
            }

            return newMarcaje

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear marcaje en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
