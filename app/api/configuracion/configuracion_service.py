from time import time

from app.api.configuracion.configuracion_repository import ConfiguracionRepository

class Configuracion_Service():
    _cache = {}
    _expira = 0

    @staticmethod
    def get_config(db, clave):
        if time() > Configuracion_Service._expira:
            configuraciones = ConfiguracionRepository.getConfiguraciones(db)

            Configuracion_Service._cache = {
                row["clave"]: row
                for row in configuraciones
            }
            Configuracion_Service._expira = time() + 300  # 5 minutos

        return Configuracion_Service._cache.get(clave)
    
    @staticmethod
    def get_value(db, clave, default=None):

        config = Configuracion_Service.get_config(db, clave)

        if not config:
            return default

        valor = config["valor"]
        tipo = config["tipo"]

        if tipo == "INT":
            return int(valor)

        if tipo == "FLOAT":
            return float(valor)

        if tipo == "BOOL":
            return str(valor).lower() in (
                "true",
                "1",
                "si",
                "sí"
            )

        return valor

    @staticmethod
    def getConfiguracionById_service(db, idConfiguracion):
        try:
            data = ConfiguracionRepository.getConfiguracionById(db, idConfiguracion)
            configuracion = {
                "idConfiguracion": data["idConfiguracion"],
                "categoria": data["categoria"],
                "clave": data["clave"],
                "valor": data["valor"],
                "tipo": data["tipo"],
                "descripcion": data["descripcion"],
            }

            return configuracion

        except Exception as ex:
            raise Exception(f"No se pudo obtener configuracion en el servicio: {str(ex)}")
    
    @staticmethod
    def getConfiguracionByCategoria_service(db, categoria):
        try:
            data = ConfiguracionRepository.getConfiguracionByCategoria(db, categoria)
            configuraciones = []
            for row in data:
                configuracion = {
                    "idConfiguracion": row["idConfiguracion"],
                    "categoria": row["categoria"],
                    "clave": row["clave"],
                    "valor": row["valor"],
                    "tipo": row["tipo"],
                    "descripcion": row["descripcion"],
                }
                configuraciones.append(configuracion)
                
            return configuraciones

        except Exception as ex:
            raise Exception(f"No se pudo obtener configuracion en el servicio: {str(ex)}")
        
    @staticmethod
    def getConfiguraciones_service(db):
        try:
            data = ConfiguracionRepository.getConfiguraciones(db)
            configuraciones = []
            for row in data:
                configuracion = {
                    "idConfiguracion": row["idConfiguracion"],
                    "categoria": row["categoria"],
                    "clave": row["clave"],
                    "valor": row["valor"],
                    "tipo": row["tipo"],
                    "descripcion": row["descripcion"],
                }

                configuracion["_saveStatus"] = "saved"
                configuracion["_isNew"] = False
                
                configuraciones.append(configuracion)
            return configuraciones

        except Exception as ex:
            raise Exception(f"No se pudo obtener configuracion en el servicio: {str(ex)}")
            
    @staticmethod
    def getConfiguracionesByClave_service(db, clave):
        try:
            data = ConfiguracionRepository.getConfiguracionesByClave(db, clave)
            configuracion = {
                "idConfiguracion": data["idConfiguracion"],
                "categoria": data["categoria"],
                "clave": data["clave"],
                "valor": data["valor"],
                "tipo": data["tipo"],
                "descripcion": data["descripcion"],
            }

            return configuracion

        except Exception as ex:
            raise Exception(f"No se pudo obtener configuracion en el servicio: {str(ex)}")
            
    @staticmethod
    def createConfiguracion_service(db, data):
        try:
            categoria = data.get("categoria")
            clave = data.get("clave")
            valor = data.get("valor")
            tipo = data.get("tipo")
            descripcion = data.get("descripcion")
            
            required_fields = {
                "categoria": categoria,
                "clave": clave,
                "valor": valor,
                "tipo": tipo,
                "descripcion": descripcion,
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            resultado = ConfiguracionRepository.createConfiguracion(db, categoria, clave, valor, tipo, descripcion)
            
            if not isinstance(resultado, dict) or "error" not in resultado:
                Configuracion_Service._cache = {}
                Configuracion_Service._expira = 0

            return resultado
        
        except Exception as ex:
            raise Exception(f"No se pudo crear el configuracion. {str(ex)}")
        
    @staticmethod
    def updateConfiguracion_service(db, data):
        try:
            idConfiguracion = data.get("idConfiguracion")
            categoria = data.get("categoria")
            clave = data.get("clave")
            valor = data.get("valor")
            tipo = data.get("tipo")
            descripcion = data.get("descripcion")

            required_fields = {
                "categoria": categoria,
                "clave": clave,
                "valor": valor,
                "tipo": tipo,
                "descripcion": descripcion,
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            resultado = ConfiguracionRepository.updateConfiguracion(db, idConfiguracion, categoria, clave, valor, tipo, descripcion)

            if not isinstance(resultado, dict) or "error" not in resultado:
                Configuracion_Service._cache = {}
                Configuracion_Service._expira = 0

            return resultado
        
        except Exception as ex:
            raise Exception(f"No se pudo modificar el configuracion. {str(ex)}")
        
    @staticmethod
    def deleteConfiguracion_service(db, data):
        try:
            idConfiguracion = data.get("idConfiguracion")
            
            if not idConfiguracion:
                return {"error": "ID del configuracion es requerido."}
            
            resultado = ConfiguracionRepository.deleteConfiguracion(db, idConfiguracion)

            if not isinstance(resultado, dict) or "error" not in resultado:
                Configuracion_Service._cache = {}
                Configuracion_Service._expira = 0

            return resultado
        
        except Exception as ex:
            raise Exception(f"No se pudo eliminar le configuracion. {str(ex)}")