import MySQLdb

class EmpleadoRepository:
    @staticmethod
    def getEmpleadoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_empleado
            WHERE idEmpleado = %s
            """

            cursor.execute(query, (id,))
            empleado = cursor.fetchone()

            return empleado
        
        except Exception as ex:
            raise Exception (f"No se pudo obtener empleado por ID en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    def getEmpleadoByBadgeNumber(db, badgeNumber):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_empleado
            WHERE badgeNumber = %s
            """

            cursor.execute(query, (badgeNumber,))
            empleado = cursor.fetchone()

            return empleado
        
        except Exception as ex:
            raise Exception (f"No se pudo obtener empleado por badge en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getEmpleados(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_empleado
            """
            cursor.execute(query)

            empleados = cursor.fetchall()

            return empleados
        
        except Exception as ex:
            raise Exception ("No se pudo obtener empleados en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def get_full_name_empleados(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT CONCAT_WS(' ',
                firstName,
                secondName,
                lastName,
                lastName2
            ) AS nombre_completo
            FROM turnos_empleado;
            """
            cursor.execute(query)

            empleados = cursor.fetchall()

            return empleados
        
        except Exception as ex:
            raise Exception ("No se pudo obtener nombres completos de empleados en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getActiveEmpleadosByDepartment(db, idDepartment):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT e.idEmpleado, e.badgeNumber, e.firstName, e.secondName, e.lastName, e.lastName2, e.position, e.idDepartment, e.activo, e.idCentro, e.idLinea, e.idProceso, h.hora_inicio, h.hora_fin
            FROM turnos_empleado AS e
            LEFT JOIN turnos_horario AS h ON e.idHorario = h.idHorario 
            WHERE e.activo = 1 AND e.idDepartment = %s
            """
            cursor.execute(query, (idDepartment,))

            empleados = cursor.fetchall()

            return empleados
        
        except Exception as ex:
            raise Exception (f"No se pudo obtener empleados activos en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, idLinea, idProceso):
        cursor = None

        try: 
            if(EmpleadoRepository.getEmpleadoById(db, idEmpleado)):
                return {"error": "ID del empleado ya existe."}
            
            if(EmpleadoRepository.getEmpleadoByBadgeNumber(db, badgeNumber)):
                return {"error": "Badge del empleado ya existe."}

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_empleado(idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, idLinea, idProceso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, idLinea, idProceso,))
            
            db.connection.commit()

            newEmpleado = {
                "idEmpleado": idEmpleado, 
                "badgeNumber": badgeNumber, 
                "firstName": firstName, 
                "secondName": secondName, 
                "lastName": lastName, 
                "lastName2": lastName2,
                "position": position, 
                "idDepartment": idDepartment,
                "activo": activo,                
                "idCentro": idCentro,
                "idLinea": idLinea,
                "idProceso": idProceso,
            }

            return {"mensaje": f"Empleado creado correctamente.",
                    "Empleado": newEmpleado
            }

        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception (f"No se pudo crear empleado en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateEmpleado(db, idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, oldIdEmpleado, idLinea, idProceso, oldBadgeNumber):
        cursor = None

        try: 
            existingId = EmpleadoRepository.getEmpleadoById(db, idEmpleado)
            existingBadgeNumber = EmpleadoRepository.getEmpleadoByBadgeNumber(db, badgeNumber)

            if existingId and int(existingId[0]) != int(oldIdEmpleado):
                return {"error": f"ID del empleado ya existe. {existingId[0]}"}
            
            if existingBadgeNumber and int(existingBadgeNumber[1]) != int(oldBadgeNumber):
                return {"error": f"Badge del empleado ya existe. {existingBadgeNumber[0]}"}

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_empleado SET idEmpleado = %s, badgeNumber = %s, firstName = %s, secondName = %s, lastName = %s, lastName2 = %s, position = %s, idDepartment = %s, activo = %s, idCentro = %s, idLinea = %s, idProceso = %s
                WHERE idEmpleado = %s
                """
            
            cursor.execute(query, (idEmpleado, badgeNumber, firstName, secondName, lastName, lastName2, position, idDepartment, activo, idCentro, idLinea, idProceso, oldIdEmpleado))
            
            db.connection.commit()

            editedEmpleado = {
                "idEmpleado": idEmpleado, 
                "badgeNumber": badgeNumber, 
                "firstName": firstName, 
                "secondName": secondName, 
                "lastName": lastName, 
                "lastName2": lastName2,
                "position": position, 
                "idDepartment": idDepartment,
                "activo": activo,             
                "idCentro": idCentro,             
            }

            return {
                "mensaje": f"Empleado modificado correctamente.",
                "Empleado": editedEmpleado
            }
        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception (f"No se pudo modificar empleado en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteEmpleado(db, idEmpleado):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_empleado
            WHERE idEmpleado = %s
            """

            cursor.execute(query, (idEmpleado,))
            db.connection.commit()
            
            return {"mensaje": "Empleado eliminado"}
        
        except Exception as ex:
            db.connection.rollback()
            raise Exception (f"error {str(ex)}")

        finally:
            if cursor:
                cursor.close()