import MySQLdb

from app.extensions.slugify import Slugify

class ConfiguracionRepository:
    @staticmethod
    def getConfiguracionById(db, idConfiguracion):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_configuracion
            WHERE idConfiguracion = %s
            """

            cursor.execute(query, (idConfiguracion,))
            configuracion = cursor.fetchone()

            return configuracion
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener el Configuracion en el repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    def getConfiguracionByCategoria(db, categoria):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_configuracion
            WHERE categoria = %s
            """

            cursor.execute(query, (categoria,))
            configuraciones = cursor.fetchall()

            return configuraciones
        
        except Exception as ex:
            raise(f"No se puede encontrar por nombre en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getConfiguraciones(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_configuracion
            """
            cursor.execute(query)

            configuraciones = cursor.fetchall()

            return configuraciones
        
        except Exception as ex:
            raise Exception(f"No se pueden listar los configuraciones en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getConfiguracionesByClave(db, clave):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_configuracion
            WHERE clave = %s
            ORDER BY clave
            """
            cursor.execute(query, (clave,))

            configuraciones = cursor.fetchall()

            return configuraciones
        
        except Exception as ex:
            raise Exception (f"No se pueden listar los configuraciones en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def createConfiguracion(db, categoria, clave, valor, tipo, descripcion):
        cursor = None

        try:
            data = ConfiguracionRepository.getConfiguraciones(db)
            slugClave = Slugify.slugify(clave)

            exists = any(
                Slugify.slugify(row["clave"]) == slugClave
                for row in data
            )

            if exists:
                return {
                    "error": f"La clave de la configuración ya existe."
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_configuracion(categoria, clave, valor, tipo, descripcion)
                VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(query, (categoria, clave, valor, tipo, descripcion,))
            
            db.connection.commit()

            newConfiguracion = {
                "idConfiguracion": cursor.lastrowid,
                "categoria": categoria,
                "clave": clave,
                "valor": valor,
                "tipo": tipo,
                "descripcion": descripcion,
            }

            return newConfiguracion

        
        except Exception as ex:
            db.connection.rollback()
            
            raise Exception(f"No se pudo crear configuracion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateConfiguracion(db, idConfiguracion, categoria, clave, valor, tipo, descripcion):
        cursor = None

        try: 
            data = ConfiguracionRepository.getConfiguraciones(db)
            idConfiguracionData = int(idConfiguracion)
            slugClave = Slugify.slugify(clave)

            exists = any(
                Slugify.slugify(row["clave"]) == slugClave
                and int(row["idConfiguracion"]) != idConfiguracionData
                for row in data
            )

            if exists:
                return {
                    "error": f"La clave de la configuración ya existe."
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_configuracion SET categoria = %s, clave = %s, valor = %s, tipo = %s, descripcion = %s
                WHERE idConfiguracion = %s
                """
            
            cursor.execute(query, (categoria, clave, valor, tipo, descripcion, idConfiguracion))
            
            db.connection.commit()

            editedConfiguracion = {
                "idConfiguracion": idConfiguracion,
                "categoria": categoria,
                "clave": clave,
                "valor": valor,
                "tipo": tipo,
                "descripcion": descripcion,       
            }

            return editedConfiguracion

        except Exception as ex:
            db.connection.rollback()
                        
            raise Exception(f"No se pudo modificar configuracion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteConfiguracion(db, idConfiguracion):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_configuracion
            WHERE idConfiguracion = %s
            """

            cursor.execute(query, (idConfiguracion,))
            db.connection.commit()
            
            return {"mensaje": "Configuracion eliminada."}
        
        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo eliminar configuracion en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()