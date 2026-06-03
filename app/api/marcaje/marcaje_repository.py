from app.extensions.slugify import Slugify

class MarcajeRepository:
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