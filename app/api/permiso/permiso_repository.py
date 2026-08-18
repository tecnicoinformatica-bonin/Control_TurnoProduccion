import MySQLdb

from app.extensions.slugify import Slugify

class PermisoRepository:
    @staticmethod
    def getPermisoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_permiso
            WHERE idPermiso = %s
            """

            cursor.execute(query, (id,))
            permiso = cursor.fetchone()

            return permiso
        
        except Exception as ex:
            return {"error": f"No se puede encontrar en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def get_permisos_asignados_por_rol(db, idRol):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT
                tp.idPermiso,
                tp.nombrePermiso,
                tp.descripcion,
                CASE
                    WHEN trp.idPermiso IS NOT NULL THEN 1
                    ELSE 0
                END AS asignado
            FROM turnos_permiso tp
            LEFT JOIN turnos_rol_permiso trp
                ON tp.idPermiso = trp.idPermiso
                AND trp.idRol = %s
            ORDER BY tp.nombrePermiso;
            """

            cursor.execute(query, (idRol,))
            
            return cursor.fetchall()
        
        except Exception as ex:
            raise Exception(f"No se puede encontrar permisos asignados por usuario en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def get_permisos_asignados_por_usuario(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT
                tp.idPermiso,
                tp.nombrePermiso,
                tp.descripcion,
                CASE
                    WHEN tup.idUsuario IS NOT NULL THEN 1
                    ELSE 0
                END AS asignado
            FROM turnos_permiso tp 
            LEFT JOIN turnos_usuario_permiso tup
                ON tup.idPermiso = tp.idPermiso  
                AND tup.idUsuario = %s
            ORDER BY tp.nombrePermiso;
            """

            cursor.execute(query, (idUsuario,))
            
            return cursor.fetchall()
        
        except Exception as ex:
            raise Exception(f"No se puede encontrar permisos asignados por usuario en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    def getPermisoByName(db, nombrePermiso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT *
            FROM turnos_permiso
            WHERE nombrePermiso = %s
            """

            cursor.execute(query, (nombrePermiso,))
            permisos = cursor.fetchall()

            return permisos
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getPermisos(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor()

            query = """
            SELECT * 
            FROM turnos_permiso
            ORDER BY nombrePermiso
            """
            cursor.execute(query)

            permisos = cursor.fetchall()

            return permisos
        
        except Exception as ex:
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createPermiso(db, nombrePermiso, descripcion):
        cursor = None

        try:
            data = PermisoRepository.getPermisos(db)
            slugNamePermiso = Slugify.slugify(nombrePermiso)

            exists = any(
                Slugify.slugify(row[1]) == slugNamePermiso
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un permiso con ese nombre: {nombrePermiso}"
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_permiso(nombrePermiso, descripcion)
                VALUES (%s, %s)
                """
            cursor.execute(query, (nombrePermiso, descripcion,))
            
            db.connection.commit()

            newPermiso = {
                "idPermiso": cursor.lastrowid, 
                "nombrePermiso": nombrePermiso,          
                "descripcion": descripcion,          
            }

            return {"mensaje": f"Línea creada correctamente. ID: {newPermiso['idPermiso']}, Nombre: {newPermiso['nombrePermiso']}, descripcion: {newPermiso['descripcion']}"}

        
        except Exception as ex:
            db.connection.rollback()
            
            return {"error": f"No se pudo crear permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updatePermiso(db, idPermiso, nombrePermiso, descripcion):
        cursor = None

        try: 
            data = PermisoRepository.getPermisos(db)
            slugNamePermiso = Slugify.slugify(nombrePermiso)

            exists = any(
                Slugify.slugify(row[1]) == slugNamePermiso and int(row[0]) != int(idPermiso)
                for row in data
            )

            if exists:
                return {
                    "error": f"Ya existe un permiso con ese nombre: {nombrePermiso}"
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_permiso SET nombrePermiso = %s, descripcion = %s
                WHERE idPermiso = %s
                """
            
            cursor.execute(query, (nombrePermiso, descripcion, idPermiso))
            
            db.connection.commit()

            editedPermiso = {
                "idPermiso": idPermiso, 
                "nombrePermiso": nombrePermiso, 
                "descripcion": descripcion,          
            }

            return {"mensaje": f"Línea modificada correctamente. ID: {editedPermiso['idPermiso']}, Nombre: {editedPermiso['nombrePermiso']}, descripcion: {editedPermiso['descripcion']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deletePermiso(db, idPermiso):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_permiso
            WHERE idPermiso = %s
            """

            cursor.execute(query, (idPermiso,))
            db.connection.commit()
            
            return {"mensaje": "Permiso eliminada."}
        
        except Exception as ex:
            db.connection.rollback()

            return {"error": f"No se pudo eliminar permiso en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()