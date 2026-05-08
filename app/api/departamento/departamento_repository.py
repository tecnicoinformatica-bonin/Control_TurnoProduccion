from app.extensions.slugify import Slugify


class DepartamentoRepository:
    @staticmethod
    def getDepartamentoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_departamento
            WHERE idDepartment = %s
            """

            cursor.execute(query, (id,))
            departamento = cursor.fetchone()

            return departamento
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getDepartamentoByName(db, name):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_departamento
            WHERE name = %s
            """

            cursor.execute(query, (name,))
            departamento = cursor.fetchone()

            return departamento
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getDepartamentos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_departamento
            ORDER BY name
            """
            cursor.execute(query)

            departamentos = cursor.fetchall()

            return departamentos
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getDepartamentos_ASC(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_departamento
            ORDER BY name 
            """
            cursor.execute(query)

            departamentos = cursor.fetchall()

            return departamentos
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getDepartamentos_aplica_horas_extra(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_departamento
            WHERE aplica_horas_extra = 1
            ORDER BY name
            """
            cursor.execute(query)

            departamentos = cursor.fetchall()

            return departamentos
        
        except Exception as ex:
            return {"error": f"No se pudo obtener departamentos en el repositorio: {str(ex)}"}
        
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createDepartamento(db, name, aplica_horas_extra):
        cursor = None

        try:
            data = DepartamentoRepository.getDepartamentoByName(db, name)
            name_DB = ""
            if data:
                name_DB = Slugify.slugify(data[1]) 
            name_slugified = Slugify.slugify(name) 
            
            if(name_DB == name_slugified):
                return {"error": "Departamento ya existe."}

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_departamento(name, aplica_horas_extra)
                VALUES (%s, %s)
                """
            
            cursor.execute(query, (name, aplica_horas_extra,))
            
            db.connection.commit()

            newDepartamento = {
                "idDepartment": cursor.lastrowid,
                "name": name,
                "aplica_horas_extra": aplica_horas_extra,
            }

            return {"mensaje": f"Departamento creado correctamente. ID: {newDepartamento['idDepartment']}, Nombre: {newDepartamento['name']}, Aplica para horas extra: {newDepartamento['aplica_horas_extra']}"}

        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo crear el departamento en el repositorio: {str(ex)}"}
        
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateDepartamento(db, idDepartment, name, aplica_horas_extra):
        cursor = None

        try: 
            data = DepartamentoRepository.getDepartamentoByName(db, name)
            name_DB = ""
            idDepartment_DB = 0
            if data:
                idDepartment_DB = int(data[0])
                name_DB = Slugify.slugify(data[1]) 

            name_slugified = Slugify.slugify(name) 

            if int(idDepartment) != idDepartment_DB and name_slugified == name_DB:
                return {"error": f"ID del departamento ya existe. {name}"}

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_departamento SET name = %s, aplica_horas_extra = %s
                WHERE idDepartment = %s
                """
            
            cursor.execute(query, (name, aplica_horas_extra, idDepartment))
            
            db.connection.commit()

            editedDepartamento = {
                "idDepartment": idDepartment,
                "name": name,
                "aplica_horas_extra": aplica_horas_extra,
            }

            return {"mensaje": f"Departamento modificado correctamente. ID: {editedDepartamento['idDepartment']}, Nombre: {editedDepartamento['name']}, Aplica para horas extra: {editedDepartamento['aplica_horas_extra']}"}

        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo modificar el departamento en el repositorio: {str(ex)}"}
        
        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteDepartamento(db, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_departamento
            WHERE idDepartment = %s
            """

            cursor.execute(query, (idDepartment,))
            db.connection.commit()
            
            return {"mensaje": "Departamento eliminado"}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo eliminar el departamento en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()