from app.extensions.slugify import Slugify

class Centro_de_costoRepository:
    @staticmethod
    def getCentro_de_costoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_centro_de_costo
            WHERE idCentro = %s
            """

            cursor.execute(query, (id,))
            centro_de_costo = cursor.fetchone()

            return centro_de_costo
        
        except Exception as ex:
            return {"error": f"No se pudo obtener centro de costo por ID en repositorio {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getCentro_de_costoByDepartment(db, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_centro_de_costo
            WHERE idDepartment = %s
            """

            cursor.execute(query, (idDepartment,))
            centro_de_costo = cursor.fetchall()

            return centro_de_costo
        
        except Exception as ex:
            return {"error": f"No se pudo obtener centro de costo por ID en repositorio {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    def getCentro_de_costoByName(db, nombreCentro):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_centro_de_costo
            WHERE nombreCentro = %s
            """

            cursor.execute(query, (nombreCentro,))
            centros_de_costo = cursor.fetchone()

            return centros_de_costo
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getCentros_de_costo(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_centro_de_costo
            """
            cursor.execute(query)

            centros_de_costo = cursor.fetchall()

            return centros_de_costo
        
        except Exception as ex:
            return {"error": f"No se pudo encontrar centros de costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createCentro_de_costo(db, nombreCentro, idDepartment):
        cursor = None

        try:
            data = Centro_de_costoRepository.getCentros_de_costo(db)
            slugNameCentro_de_costo = Slugify.slugify(nombreCentro)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el nombreCentro """
            exists = any(
                int(row[2]) == idDepartment and Slugify.slugify(row[1]) == slugNameCentro_de_costo
                for row in data
            )

            if exists:
                return {
                    "error": f"El centro de costo ya existe para ese departamento: {nombreCentro} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_centro_de_costo(nombreCentro, idDepartment)
                VALUES (%s, %s)
                """
            cursor.execute(query, (nombreCentro, idDepartment,))
            
            db.connection.commit()

            newCentro_de_costo = {
                "idCentro": cursor.lastrowid, 
                "nombreCentro": nombreCentro,          
                "idDepartment": idDepartment,          
            }

            return {"mensaje": f"Línea creada correctamente. ID: {newCentro_de_costo['idCentro']}, Nombre: {newCentro_de_costo['nombreCentro']}, idDepartment: {newCentro_de_costo['idDepartment']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear centro de costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateCentro_de_costo(db, idCentro, nombreCentro, idDepartment):
        cursor = None

        try: 
            data = Centro_de_costoRepository.getCentros_de_costo(db)
            slugNameCentro_de_costo = Slugify.slugify(nombreCentro)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el nombreCentro """
            exists = any(
                int(row[2]) == idDepartment and slugNameCentro_de_costo == Slugify.slugify(row[1]) and idCentro != int(row[0])
                for row in data
            )

            if exists:
                return {
                    "error": f"El centro de costo ya existe para ese departamento: {nombreCentro} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_centro_de_costo SET nombreCentro = %s, idDepartment = %s
                WHERE idCentro = %s
                """
            
            cursor.execute(query, (nombreCentro, idDepartment, idCentro))
            
            db.connection.commit()

            editedCentro_de_costo = {
                "idCentro": idCentro, 
                "nombreCentro": nombreCentro, 
                "idDepartment": idDepartment,          
            }

            return {"mensaje": f"Línea modificada correctamente. ID: {editedCentro_de_costo['idCentro']}, Nombre: {editedCentro_de_costo['nombreCentro']}, idDepartment: {editedCentro_de_costo['idDepartment']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar centro de costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteCentro_de_costo(db, idCentro):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_centro_de_costo
            WHERE idCentro = %s
            """

            cursor.execute(query, (idCentro,))
            db.connection.commit()
            
            return {"mensaje": "Centro de costo eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar centro de costo en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()