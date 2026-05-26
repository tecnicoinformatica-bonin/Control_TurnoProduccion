from app.extensions.slugify import Slugify

class LineaRepository:
    @staticmethod
    def getLineaById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_linea
            WHERE idLinea = %s
            """

            cursor.execute(query, (id,))
            linea = cursor.fetchone()

            return linea
        
        except Exception as ex:
            print(ex)
            return None

        finally:
            if cursor:
                cursor.close()

    def getLineaByName(db, nameLinea):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_linea
            WHERE nameLinea = %s
            """

            cursor.execute(query, (nameLinea,))
            lineas = cursor.fetchall()

            return lineas
        
        except Exception as ex:
            
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getLineas(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_linea
            """
            cursor.execute(query)

            lineas = cursor.fetchall()

            return lineas
        
        except Exception as ex:
            print(ex)
            return None

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createLinea(db, nameLinea, idDepartment, minimo_requerido):
        cursor = None

        try:
            data = LineaRepository.getLineas(db)
            slugNameLinea = Slugify.slugify(nameLinea)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el nameLinea """
            exists = any(
                int(row[2]) == idDepartment and Slugify.slugify(row[1]) == slugNameLinea
                for row in data
            )

            if exists:
                return {
                    "error": f"La línea ya existe para ese departamento: {nameLinea} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_linea(nameLinea, idDepartment, minimo_requerido)
                VALUES (%s, %s, %s)
                """
            cursor.execute(query, (nameLinea, idDepartment, minimo_requerido,))
            
            db.connection.commit()

            newLinea = {
                "idLinea": cursor.lastrowid, 
                "nameLinea": nameLinea,
                "idDepartment": idDepartment,
                "minimo_requerido": minimo_requerido,
            }

            return {"mensaje": f"Línea creada correctamente. ID: {newLinea['idLinea']}, Nombre: {newLinea['nameLinea']}, idDepartment: {newLinea['idDepartment']} Mínimo requerido: {newLinea['minimo_requerido']}"}

        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo crear linea en repositorio: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateLinea(db, idLinea, nameLinea, idDepartment, minimo_requerido):
        cursor = None

        try: 
            data = LineaRepository.getLineas(db)
            slugNameLinea = Slugify.slugify(nameLinea)
            idDepartment = int(idDepartment)

            """  Row[2] is the idDepartment an row[1] es el nameLinea """
            exists = any(
                int(row[0]) != idLinea 
                and int(row[2]) == idDepartment 
                and Slugify.slugify(row[1]) == slugNameLinea
                for row in data
            )

            if exists:
                return {
                    "error": f"La línea ya existe para ese departamento: {nameLinea} en departamento ID {idDepartment}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_linea SET nameLinea = %s, idDepartment = %s, minimo_requerido = %s
                WHERE idLinea = %s
                """
            
            cursor.execute(query, (nameLinea, idDepartment, minimo_requerido, idLinea,))
            
            db.connection.commit()

            editedLinea = {
                "idLinea": idLinea,
                "nameLinea": nameLinea,
                "idDepartment": idDepartment,
                "minimo_requerido": minimo_requerido,
            }

            return {"mensaje": f"Línea modificada correctamente. ID: {editedLinea['idLinea']}, Nombre: {editedLinea['nameLinea']}, idDepartment: {editedLinea['idDepartment']}, Mínimo requerido: {editedLinea['minimo_requerido']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            raise Exception (f"No se pudo modificar linea en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteLinea(db, idLinea):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_linea
            WHERE idLinea = %s
            """

            cursor.execute(query, (idLinea,))
            db.connection.commit()
            
            return {"mensaje": "Linea eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar linea en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()