from app.extensions.slugify import Slugify

class RegistroRepository:
    @staticmethod
    def getRegistroById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idRegistro = %s
            """

            cursor.execute(query, (id,))
            registro = cursor.fetchone()

            return registro
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el registro en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRegistrosByProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idProgramacion en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByEmpleado(db, idEmpleado):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idEmpleado = %s
            """

            cursor.execute(query, (idEmpleado,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idEmpleado en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByEmpleadoAndProgramacion(db, idEmpleado, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idEmpleado = %s AND idProgramacion = %s
            """

            cursor.execute(query, (idEmpleado, idProgramacion,))
            registro = cursor.fetchone()

            return registro
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por Empleado y Programación en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByBadgeNumber(db, badgeNumber):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE badgeNumber = %s
            """

            cursor.execute(query, (badgeNumber,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por badgeNumber en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByBadgeNumberAndProgramacion(db, badgeNumber, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE badgeNumber = %s AND idProgramacion = %s
            """

            cursor.execute(query, (badgeNumber, idProgramacion,))
            registro = cursor.fetchone()

            return registro
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por BadgeNumber y Programación en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByLinea(db, idLinea):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idLinea = %s
            """

            cursor.execute(query, (idLinea,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idLinea en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByLineaAndProgramacion(db, idLinea, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idLinea = %s AND idProgramacion = %s
            """

            cursor.execute(query, (idLinea, idProgramacion,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por Línea y Programación en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
   
    @staticmethod
    def getRegistroByProceso(db, idProceso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idProceso = %s
            """

            cursor.execute(query, (idProceso,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por idProceso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByProcesoAndProgramacion(db, idProceso, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idProceso = %s AND idProgramacion = %s
            """

            cursor.execute(query, (idProceso, idProgramacion,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por Proceso y Programación en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByCentro(db, idCentro):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idCentro = %s
            """

            cursor.execute(query, (idCentro,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por centro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getRegistroByCentroAndProgramacion(db, idCentro, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_registro
            WHERE idCentro = %s AND idProgramacion = %s
            """

            cursor.execute(query, (idCentro, idProgramacion,))
            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por Centro y Programación en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCount_aplica_cena_porProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT COUNT(aplica_cena) as Cuenta_si_cena
            FROM turnos_registro
            WHERE aplica_cena = 1 AND idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            conteo = cursor.fetchone()

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede realizar conteo de cenas con costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCount_no_aplica_cena_porProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT COUNT(aplica_cena)
            FROM turnos_registro
            WHERE aplica_cena = 0 AND idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            conteo = cursor.fetchone()

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede realizar conteo de cenas sin costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCount_aplica_almuerzo_porProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT COUNT(aplica_almuerzo)
            FROM turnos_registro
            WHERE aplica_almuerzo = 1 AND idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            conteo = cursor.fetchone()

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede realizar conteo de almuerzos sin costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCount_aplica_transporte_porProgramacion(db, idProgramacion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT COUNT(aplica_transporte)
            FROM turnos_registro
            WHERE aplica_transporte = 1 AND idProgramacion = %s
            """

            cursor.execute(query, (idProgramacion,))
            conteo = cursor.fetchone()

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede realizar conteo de aplica transporte en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRegistros(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_registro
            """
            cursor.execute(query)

            registros = cursor.fetchall()

            return registros
        
        except Exception as ex:
            return {"error": f"No se pueden listar los registros en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def createRegistro(db, idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber):
        cursor = None

        try:
            data = RegistroRepository.getRegistroByEmpleadoAndProgramacion(db, idEmpleado, idProgramacion)
            
            if data:
                return {
                    "error": f"El registro para el Usuario ya existe en la programación."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_registro(idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber))
            
            db.connection.commit()

            newRegistro = {
                "idRegistro": cursor.lastrowid, 
                "idProgramacion": idProgramacion,
                "idEmpleado": idEmpleado,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
                "aplica_almuerzo": aplica_almuerzo,
                "aplica_cena": aplica_cena,
                "aplica_transporte": aplica_transporte,
                "observacion_transporte": observacion_transporte,
                "fecha": fecha,
                "idCentro": idCentro,
                "badgeNumber": badgeNumber,
            }

            return {"mensaje": f"Registro creado correctamente. ID: {newRegistro['idRegistro']}, ID Programacion: {newRegistro['idProgramacion']}, ID Empleado: {newRegistro['idEmpleado']}"}
        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear registro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateRegistro(db, idRegistro, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber):
        cursor = None

        try: 
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_registro SET idEmpleado = %s, hora_inicio = %s, hora_fin = %s, idLinea = %s, idProceso = %s, aplica_almuerzo = %s, aplica_cena = %s, aplica_transporte = %s, observacion_transporte = %s, fecha = %s, idCentro = %s, badgeNumber = %s
                WHERE idRegistro = %s
                """
            
            cursor.execute(query, (idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber, idRegistro,))
            
            db.connection.commit()

            editedRegistro = {
                "idEmpleado": idEmpleado,
                "idRegistro": idRegistro,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
                "aplica_almuerzo": aplica_almuerzo,
                "aplica_cena": aplica_cena,
                "aplica_transporte": aplica_transporte,
                "observacion_transporte": observacion_transporte,          
                "fecha": fecha,
                "idCentro": idCentro,
                "badgeNumber": badgeNumber,
            }

            return {"mensaje": f"Registro modificado correctamente. ID: {editedRegistro['idRegistro']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar registro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteRegistro(db, idRegistro):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_registro
            WHERE idRegistro = %s
            """

            cursor.execute(query, (idRegistro,))
            db.connection.commit()
            
            return {"mensaje": "Registro eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar registro en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()