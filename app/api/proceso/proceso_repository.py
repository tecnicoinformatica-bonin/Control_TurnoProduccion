from app.extensions.slugify import Slugify

class ProcesoRepository:
    @staticmethod
    def getProcesoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_proceso
            WHERE idProceso = %s
            """

            cursor.execute(query, (id,))
            proceso = cursor.fetchone()

            return proceso
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el Proceso en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    def getProcesoByName(db, proceso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_proceso
            WHERE proceso = %s
            """

            cursor.execute(query, (proceso,))
            procesos = cursor.fetchall()

            return procesos
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getProcesos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_proceso
            """
            cursor.execute(query)

            procesos = cursor.fetchall()

            return procesos
        
        except Exception as ex:
            return {"error": f"No se pueden listar los procesos en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createProceso(db, proceso, idDepartment):
        cursor = None

        try:
            data = ProcesoRepository.getProcesos(db)
            slugNameProceso = Slugify.slugify(proceso)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el proceso """
            exists = any(
                int(row[2]) == idDepartment and Slugify.slugify(row[1]) == slugNameProceso
                for row in data
            )

            if exists:
                return {
                    "error": f"El proceso ya existe para ese departamento: {proceso} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_proceso(proceso, idDepartment)
                VALUES (%s, %s)
                """
            cursor.execute(query, (proceso, idDepartment,))
            
            db.connection.commit()

            newProceso = {
                "idProceso": cursor.lastrowid, 
                "proceso": proceso,          
                "idDepartment": idDepartment,          
            }

            return {"mensaje": f"Proceso creado correctamente. ID: {newProceso['idProceso']}, Nombre: {newProceso['proceso']}, idDepartment: {newProceso['idDepartment']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear proceso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateProceso(db, idProceso, proceso, idDepartment):
        cursor = None

        try: 
            data = ProcesoRepository.getProcesos(db)
            slugNameProceso = Slugify.slugify(proceso)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el proceso """
            exists = any(
                int(row[2]) == idDepartment and Slugify.slugify(row[1]) == slugNameProceso
                for row in data
            )

            if exists:
                return {
                    "error": f"El proceso ya existe para ese departamento: {proceso} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_proceso SET proceso = %s, idDepartment = %s
                WHERE idProceso = %s
                """
            
            cursor.execute(query, (proceso, idDepartment, idProceso))
            
            db.connection.commit()

            editedProceso = {
                "idProceso": idProceso, 
                "proceso": proceso, 
                "idDepartment": idDepartment,          
            }

            return {"mensaje": f"Proceso modificado correctamente. ID: {editedProceso['idProceso']}, Nombre: {editedProceso['proceso']}, idDepartment: {editedProceso['idDepartment']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar proceso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteProceso(db, idProceso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_proceso
            WHERE idProceso = %s
            """

            cursor.execute(query, (idProceso,))
            db.connection.commit()
            
            return {"mensaje": "Proceso eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar proceso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()