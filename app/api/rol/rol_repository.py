from app.extensions.slugify import Slugify

class RolRepository:
    @staticmethod
    def getRolById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_rol
            WHERE idRol = %s
            """

            cursor.execute(query, (id,))
            rol = cursor.fetchone()

            return rol
        
        except Exception as ex:
            return {"error": f"No se pudo obtener el rol en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    def getRolByName(db, nombre):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_rol
            WHERE nombre = %s
            """

            cursor.execute(query, (nombre,))
            roles = cursor.fetchall()

            return roles
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getRoles(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_rol
            """
            cursor.execute(query)

            roles = cursor.fetchall()

            return roles
        
        except Exception as ex:
            return {"error": f"No se pueden listar los roles en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createRol(db, nombre, descripcion):
        cursor = None

        try:
            data = RolRepository.getRoles(db)
            slugNombre = Slugify.slugify(nombre)

            """  Row[2] is the descripcion an row[1] es el rol """
            exists = any(
                Slugify.slugify(row[1]) == slugNombre
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {nombre} ya existe."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_rol(nombre, descripcion)
                VALUES (%s, %s)
                """
            cursor.execute(query, (nombre, descripcion,))
            
            db.connection.commit()

            newRol = {
                "idRol": cursor.lastrowid, 
                "nombre": nombre,          
                "descripcion": descripcion,          
            }

            return {"mensaje": f"Rol creado correctamente. ID: {newRol['idRol']}, Nombre: {newRol['nombre']}, descripcion: {newRol['descripcion']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateRol(db, idRol, nombre, descripcion):
        cursor = None

        try: 
            data = RolRepository.getRoles(db)
            slugNombre = Slugify.slugify(nombre)

            """  Row[2] is the descripcion an row[1] es el nombre """
            exists = any(
                Slugify.slugify(row[1]) == slugNombre and int(row[0]) != idRol
                for row in data
            )

            if exists:
                return {
                    "error": f"El rol {nombre} ya existe"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_rol SET nombre = %s, descripcion = %s
                WHERE idRol = %s
                """
            
            cursor.execute(query, (nombre, descripcion, idRol))
            
            db.connection.commit()

            editedRol = {
                "idRol": idRol, 
                "nombre": nombre, 
                "descripcion": descripcion,          
            }

            return {"mensaje": f"Rol modificado correctamente. ID: {editedRol['idRol']}, Nombre: {editedRol['nombre']}, descripcion: {editedRol['descripcion']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteRol(db, idRol):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_rol
            WHERE idRol = %s
            """

            cursor.execute(query, (idRol,))
            db.connection.commit()
            
            return {"mensaje": "Rol eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar rol en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()