import MySQLdb

class FeriadoRepository:
    @staticmethod
    def getFeriadoById(db, id):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_calendario_feriados
            WHERE idFeriado = %s
            """

            cursor.execute(query, (id,))
            feriado = cursor.fetchone()

            return feriado
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener feriado: {str(ex)}")

        finally:
            if cursor:
                cursor.close()

    def getFeriadoByName(db, nombre):
        cursor = None

        try:
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT *
            FROM turnos_calendario_feriados
            WHERE nombre = %s
            """

            cursor.execute(query, (nombre,))
            feriados = cursor.fetchall()

            return feriados
        
        except Exception as ex:
            
            return {"error": f"No se puede encontrar por nombre en repositorio: {str(ex)}"}

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getFeriados(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_calendario_feriados
            """
            cursor.execute(query)

            feriados = cursor.fetchall()

            return feriados
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener feriados: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getFeriados_dia_completo(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_calendario_feriados
            WHERE es_medio_dia = 0
            """
            cursor.execute(query)

            feriados = cursor.fetchall()

            return feriados
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener feriados: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def getFeriados_medio_dia(db):
        cursor = None
        
        try: 
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
            SELECT * 
            FROM turnos_calendario_feriados
            WHERE es_medio_dia = 1
            """
            cursor.execute(query)

            feriados = cursor.fetchall()

            return feriados
        
        except Exception as ex:
            raise Exception(f"No se pudo obtener feriados: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
    
    @staticmethod
    def createFeriado(db, fecha, nombre, tipo, es_medio_dia):
        cursor = None

        try:
            data = FeriadoRepository.getFeriados(db)
            
            exists = any(
                row["fecha"] == fecha 
                for row in data
            )

            if exists:
                return {
                    "error": f"La fecha ya existe: {fecha} {nombre} "
                }

            cursor = db.connection.cursor()
            
            query = """
                INSERT INTO turnos_calendario_feriados(fecha, nombre, tipo, es_medio_dia)
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(query, (fecha, nombre, tipo, es_medio_dia,))
            
            db.connection.commit()

            newFeriado = {
                "idFeriado": cursor.lastrowid, 
                "fecha": fecha,
                "nombre": nombre,
                "tipo": tipo,
                "es_medio_dia": es_medio_dia,
            }

            return {
                "success": True,
                "resultado": newFeriado
            }

        except Exception as ex:
            db.connection.rollback()
            raise Exception(f"No se pudo crear feriado en repositorio: {str(ex)}")
            
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def updateFeriado(db, idFeriado, fecha, nombre, tipo, es_medio_dia):
        cursor = None

        try: 
            data = FeriadoRepository.getFeriados(db)
            
            exists = any(
                int(row["idFeriado"]) != int(idFeriado )
                and row["fecha"] == fecha 
                for row in data
            )

            if exists:
                return {
                    "error": f"La fecha ya existe: {fecha} {nombre} "
                }

            cursor = db.connection.cursor()
            
            query = """
                UPDATE turnos_calendario_feriados SET fecha = %s, nombre = %s,  tipo = %s, es_medio_dia = %s
                WHERE idFeriado = %s
                """
            
            cursor.execute(query, (fecha, nombre, tipo, es_medio_dia, idFeriado,))
            
            db.connection.commit()

            editedFeriado = {
                "idFeriado": idFeriado,
                "fecha": fecha,
                "nombre": nombre,
                "tipo": tipo,
                "es_medio_dia": es_medio_dia,
            }

            return {
                "success": True,
                "resultado": editedFeriado
            }

        except Exception as ex:
            db.connection.rollback()
                        
            raise Exception (f"No se pudo modificar feriado en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()
        
    @staticmethod
    def deleteFeriado(db, idFeriado):
        cursor = None

        try:
            cursor = db.connection.cursor()

            query = """
            DELETE FROM turnos_calendario_feriados
            WHERE idFeriado = %s
            """

            cursor.execute(query, (idFeriado,))
            db.connection.commit()
            
            return {
                "success": True,
            }
        
        except Exception as ex:
            db.connection.rollback()
            raise Exception (f"No se pudo eliminar feriado en repositorio: {str(ex)}")

        finally:
            if cursor:
                cursor.close()