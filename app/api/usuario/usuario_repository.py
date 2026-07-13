import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

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
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT idUsuario, username, nombre, password_hash, activo, scope_departamentos_global, scope_permisos_global, cambiar_password

            FROM turnos_usuario
            WHERE username = %s
            """
            cursor.execute(query, (username,))
            usuario = cursor.fetchone()

            return usuario

        except Exception as ex:
            return {"error": f"No se pudo obtener el usuario en el repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getUsuarioById(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT idUsuario, username, nombre, password_hash, activo, scope_departamentos_global, scope_permisos_global, cambiar_password
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
            SELECT DISTINCT nombrePermiso
            FROM (
                -- permisos directos
                SELECT p.nombrePermiso
                FROM turnos_permiso p
                JOIN turnos_usuario_permiso up
                    ON p.idPermiso = up.idPermiso
                WHERE up.idUsuario = %s

                UNION

                -- permisos por rol
                SELECT p.nombrePermiso
                FROM turnos_permiso p
                JOIN turnos_rol_permiso rp
                    ON p.idPermiso = rp.idPermiso
                JOIN turnos_usuario_rol ur
                    ON rp.idRol = ur.idRol
                WHERE ur.idUsuario = %s
                
            ) permisos
            """

            cursor.execute(query, (idUsuario, idUsuario))
            rows = cursor.fetchall()

            if rows is not None:
                permisos = [row[0] for row in rows]

            return permisos
        
        except Exception as ex:
            raise Exception(f"No se puede obtener permisos: {str(ex)}")
                    
        finally: 
            if cursor:
                cursor.close()
    
    @staticmethod
    def getUserDepartmentsById(db, idUsuario):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            SELECT d.idDepartment, d.name
            FROM turnos_departamento d
            JOIN turnos_usuario_departamento ud ON d.idDepartment  = ud.idDepartment 
            WHERE ud.idUsuario  = %s
            """

            cursor.execute(query, (idUsuario,))
            rows = cursor.fetchall()

            departamentos = [
                {
                    "idDepartment": row[0], 
                    "name": row[1]
                } 
                
                for row in rows
            ]
            
            return departamentos
        
        except Exception as ex:
            return {"error": f"No se pueden obtener departamentos del usuario en el repositorio: {str(ex)}"}
                    
        finally: 
            if cursor:
                cursor.close()
    
    @staticmethod
    def get_usuarios_by_department_assigned(db, idDepartment):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT ts.idUsuario, ts.nombre
            FROM turnos_usuario ts
            INNER JOIN 
                turnos_usuario_departamento tud
                ON tud.idUsuario = ts.idUsuario
            WHERE tud.idDepartment = %s
            """

            cursor.execute(query, (idDepartment,))
            
            usuarios = cursor.fetchall()

            return usuarios
        
        except Exception as ex:
            raise Exception(f"No se pueden obtener departamentos del usuario en el repositorio: {str(ex)}")
                    
        finally: 
            if cursor:
                cursor.close()

    @staticmethod
    def createUsuario(db, username, nombre, password, activo, scope_departamentos_global, scope_permisos_global):
        cursor = None

        try:
            if(UsuarioRepository.getUsuarioByUsername(db, username)): 
                return {"error": "Nombre de usuario ya existe."}

            cursor = db.connection.cursor()
            hashedPassword = generate_password_hash(password)

            query = """
                INSERT INTO turnos_usuario(username, nombre, password_hash, activo, scope_departamentos_global, scope_permisos_global) 
                VALUES(%s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query, (username, nombre, hashedPassword, activo, scope_departamentos_global, scope_permisos_global,))

            db.connection.commit()

            newUser = {
                "idUsuario": cursor.lastrowid,
                "username": username,
                "nombre": nombre,   
                "activo": activo,
                "scope_departamentos_global": scope_permisos_global,
                "scope_permisos_global": scope_departamentos_global,
            }

            return {"mensaje": 
                    f"""
                    Usuario creado correctamente. 
                        ID: {newUser['idUsuario']}, 
                        Usuario: {newUser['username']},
                        Nombre: {newUser['nombre']}, 
                        Activo: {newUser['activo']},
                        Scope_depts: {newUser['scope_departamentos_global']},
                        Scope_permission: {newUser['scope_permisos_global']},
                    """}
        
        except Exception as ex:
            db.connection.rollback()
            raise Exception (f"No se puede crear el usuario: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateUsuario(db, idUsuario, nombre, activo, scope_departamentos_global, scope_permisos_global):
        cursor = None

        if scope_departamentos_global == 1 or scope_departamentos_global == True or scope_departamentos_global == "True":
            scope_departamentos_global = 1
        else:
            scope_departamentos_global = 0
        
        if scope_permisos_global == 1 or scope_permisos_global == True or scope_permisos_global == "True":
            scope_permisos_global = 1
        else:
            scope_permisos_global = 0

        try: 
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario SET nombre = %s, activo = %s, scope_departamentos_global = %s, scope_permisos_global = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (nombre, activo, scope_departamentos_global, scope_permisos_global, idUsuario))
            
            db.connection.commit()

            editedUsuario = {
                "idUsuario": idUsuario,
                "nombre": nombre,   
                "activo": activo,
                "scope_departamentos_global": scope_departamentos_global,
                "scope_permisos_global": scope_permisos_global,
            }

            return {"mensaje": 
                    f"""
                    Usuario creado correctamente. 
                        ID: {editedUsuario['idUsuario']}, 
                        Nombre: {editedUsuario['nombre']}, 
                        Activo: {editedUsuario['activo']},
                        Scope_depts: {editedUsuario['scope_departamentos_global']},
                        Scope_permission: {editedUsuario['scope_permisos_global']},
                    """}

        except Exception as ex:
            db.connection.rollback()
            raise Exception (f"No se puede crear el usuario: {str(ex)}")

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

            return {
                "mensaje": f"Contraseña modificada correctamente. ID de usuario: {editedUsuario['idUsuario']}",
                "resultado": editedUsuario
            }

        except Exception as ex:
            db.connection.rollback()
                        
            return {"error": f"No se pudo modificar contraseña en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def change_status_cambiar_password(db, idUsuario, cambiar_password):
        cursor = None

        try: 
            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_usuario SET cambiar_password = %s
                WHERE idUsuario = %s
                """
            
            cursor.execute(query, (cambiar_password, idUsuario))
            
            db.connection.commit()

            editedUsuario = {
                "idUsuario": idUsuario,
                "cambiar_password": cambiar_password,
            }

            return editedUsuario

        except Exception as ex:
            db.connection.rollback()
                        
            raise Exception(f"No se pudo cambiar el estado del campo cambiar_password: {str(ex)}")

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