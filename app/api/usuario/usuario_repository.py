from werkzeug.security import generate_password_hash, check_password_hash

from app.api.usuario.usuario_model import Usuario_Rutas
from app.extensions.slugify import Slugify

class UsuarioRepository:
    @staticmethod
    def getUsuarios(db):
        cursor = None

        try:
            cursor = db.connection.cursor()
            query = """
                SELECT * 
                FROM turnos_usuario
                """
            cursor.execute(query)
            usuarios = cursor.fetchall()
            
            return usuarios
        
        except Exception as ex:
            return {"error": f"No se pudo obtener usuarios en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
            
    @staticmethod
    def getUsuarioByUsername(db, username):
        
        cursor = None

        try:
            cursor = db.connection.cursor()
            query = """
                SELECT idUsuario 
                FROM turnos_usuario
                WHERE username = %s
                """
            cursor.execute(query, (username,))
            idUsuario = cursor.fetchone()
            
            if idUsuario:
                return idUsuario is not None
        
        except Exception as ex:
            return {"error": f"No se pudo determinar si el usuario existe en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getUsuarioById(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT idUsuario, username, nombre, password_hash, activo

            FROM turnos_usuario
            WHERE idUsuario = %s
            """
            cursor.execute(query, (idUsuario,))
            usuario = cursor.fetchone()

            return usuario

        except Exception as ex:
            return {"error": f"No se pudo obtener el usuario en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getUserPaths(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT r.path
            FROM turnos_ruta r
            JOIN turnos_rol_ruta rr ON r.idRuta = rr.idRuta
            JOIN turnos_usuario_rol ur ON rr.idRol = ur.idRol
            WHERE ur.idUsuario  = %s
            """

            cursor.execute(query, (idUsuario,))
            rows = cursor.fetchall()

            if rows is not None:
                paths = [row[0] for row in rows]

            return paths
        
        except Exception as ex:
            return {"error": f"No se pueden obtener rutas del usuario en el repositorio: {str(ex)}"}
                    
        finally: 
            if cursor:
                cursor.close()

    @staticmethod
    def getUserRolesById(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT r.nombre
            FROM turnos_rol r
            JOIN turnos_usuario_rol ur ON r.idRol = ur.idRol
            WHERE ur.idUsuario  = %s
            """

            cursor.execute(query, (idUsuario,))
            rows = cursor.fetchall()

            if rows is not None:
                roles = [row[0] for row in rows]

            return roles
        
        except Exception as ex:
            return {"error": f"No se pueden obtener roles del usuario en el repositorio: {str(ex)}"}
                    
        finally: 
            if cursor:
                cursor.close()
    
    @staticmethod
    def getUserPermissionsById(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT p.nombrePermiso
            FROM turnos_permiso p
            JOIN turnos_usuario_permiso up ON p.idPermiso = up.idPermiso
            WHERE up.idUsuario  = %s
            """

            cursor.execute(query, (idUsuario,))
            rows = cursor.fetchall()

            if rows is not None:
                roles = [row[0] for row in rows]

            return roles
        
        except Exception as ex:
            return {"error": f"No se pueden obtener roles del usuario en el repositorio: {str(ex)}"}
                    
        finally: 
            if cursor:
                cursor.close()

    @staticmethod
    def createUsuario(db, username, nombre, password, activo):
        cursor = None

        try:
            if(UsuarioRepository.getUsuarioByUsername(db, username)): 
                return {"error": "Nombre de usuario ya existe."}

            cursor = db.connection.cursor()
            hashedPassword = generate_password_hash(password)

            query = """
                INSERT INTO turnos_usuario(username, nombre, password_hash, activo) 
                VALUES(%s, %s, %s, %s)
                """
            cursor.execute(query, (username, nombre, hashedPassword, activo))

            db.connection.commit()

            newUser = {
                "idUsuario": cursor.lastrowid,
                "username": username,
                "nombre": nombre,   
                "activo": activo,
            }

            return {"mensaje": f"Usuario creado correctamente. ID: {newUser['idUsuario']}, Usuario: {newUser['username']}, Nombre: {newUser['nombre']}, Activo: {newUser['activo']}"}
        
        except Exception as ex:
            db.connection.rollback()
            return {"error": f"No se pudo crear el usuario en el repositorio: {str(ex)}"}
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateUsuario(db, idUsuario, nombre, activo):
        cursor = None

        try: 
            """ [_, username_db, _, _, _] = UsuarioRepository.getUsuarioByUsername(db)
            username_db = Slugify.slugify(username_db)
            slugUsername = Slugify.slugif)

            if UsuarioRepository.getUsuarioByUsername(db) and username_db != slugUsername:
                return {
                    "error": f"El usuario} ya existe."
                }
            """
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario SET nombre = %s, activo = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (nombre, activo, idUsuario))
            
            db.connection.commit()

            editedUsuario = {
                "idUsuario": idUsuario,
                "nombre": nombre,
                "activo": activo
            }

            return {"mensaje": f"Usuario modificado correctamente. ID: {editedUsuario['idUsuario']}, {editedUsuario['nombre']}, {editedUsuario['activo']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar usuario en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updatePassword(db, idUsuario, password):
        cursor = None

        try: 
            hashedPassword = generate_password_hash(password)

            """  Row[2] is the descripcion an row[1] es el path """
            
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario SET password_hash = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (hashedPassword, idUsuario))
            
            db.connection.commit()

            editedUsuario = {
                "idUsuario": idUsuario,
            }

            return {"mensaje": f"Contraseña modificada correctamente. ID de usuario: {editedUsuario['idUsuario']}"}

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar contraseña en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteUsuario(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_usuario
            WHERE idUsuario = %s
            """

            cursor.execute(query, (idUsuario,))
            db.connection.commit()
            
            return {"mensaje": "Usuario eliminado."}
        
        except Exception as ex:
            db.connection.rollback()
            print(ex)
            return {"error": f"No se pudo eliminar usuario AAA en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()