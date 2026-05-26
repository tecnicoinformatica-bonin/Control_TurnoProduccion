from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.linea.linea_service import Linea_Service
from app.api.proceso.proceso_service import Proceso_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro_log.registro_log_repository import Registro_logRepository

import traceback
from app.extensions.beneficios import calcular_beneficios

class Registro_log_Service():
    @staticmethod
    def getRegistro_logById_service(db, id):
        try:
            data = Registro_logRepository.getRegistro_logById(db, id)
            
            registro_log = {
                "idLog": data["idLog"],
                "idRegistro": data["idRegistro"],
                "idUsuario": data["idUsuario"],
                "fecha_modificacion": data["fecha_modificacion"],
                "campo_modificado": data["campo_modificado"],
                "valor_anterior": data["valor_anterior"],
                "valor_nuevo": data["valor_nuevo"],
            }
            
            return registro_log

        except Exception as ex:
            return {"error": f"No se puede obtener log desde el servicio: {str(ex)}"}
        
    @staticmethod
    def getRegistros_log_service(db):
        try:
            data = Registro_logRepository.getRegistros_log(db)
            registros_log = []
            for row in data:
                registro_log = {
                    "idLog": row["idLog"],
                    "idRegistro": row["idRegistro"],
                    "idUsuario": row["idUsuario"],
                    "fecha_modificacion": ["fecha_modificacion"],
                    "campo_modificado": ["campo_modificado"],
                    "valor_anterior": row["valor_anterior"],
                    "valor_nuevo": row["valor_nuevo"],
                }
                registros_log.append(registro_log)
            return registros_log

        except Exception as ex:
            return {"error": f"No se puede obtener registro_logs_log desde el servicio: {str(ex)}"}
            
    @staticmethod
    def getRegistros_logByRegistro_service(db, idRegistro):
        try:
            data = Registro_logRepository.getRegistros_logByRegistro(db, idRegistro)
            registros_log = []
            for row in data:
                registro_log = {
                    "idLog": row["idLog"],
                    "idRegistro": row["idRegistro"],
                    "idUsuario": row["idUsuario"],
                    "fecha_modificacion": row["fecha_modificacion"],
                    "campo_modificado": row["campo_modificado"],
                    "valor_anterior": row["valor_anterior"],
                    "valor_nuevo": row["valor_nuevo"],
                }
                registros_log.append(registro_log)
            return registros_log

        except Exception as ex:
            return {"error": f"No se puede obtener registro_logs_log desde el servicio: {str(ex)}"}
    
    @staticmethod
    def getRegistros_logByUsuario_service(db, idUsuario):
        try:
            data = Registro_logRepository.getRegistro_logByUsuario(db, idUsuario)
            registros_log = []
            for row in data:
                registro_log = {
                    "idLog": row["idLog"],
                    "idRegistro": row["idRegistro"],
                    "idUsuario": row["idUsuario"],
                    "fecha_modificacion": row["fecha_modificacion"],
                    "campo_modificado": row["campo_modificado"],
                    "valor_anterior": row["valor_anterior"],
                    "valor_nuevo": row["valor_nuevo"],
                }
                registros_log.append(registro_log)
            return registros_log

        except Exception as ex:
            return {"error": f"No se puede obtener registro_logs_log desde el servicio: {str(ex)}"}
    
    @staticmethod
    def getRegistro_logByRegistroAndUsuario_service(db, idRegistro, idUsuario):
        try:
            data = Registro_logRepository.getRegistro_logByRegistroAndUsuario(db, idRegistro, idUsuario)
            registros_log = []
            for row in data:
                registro_log = {
                    "idLog": row["idLog"],
                    "idRegistro": row["idRegistro"],
                    "idUsuario": row["idUsuario"],
                    "fecha_modificacion": row["fecha_modificacion"],
                    "campo_modificado": row["campo_modificado"],
                    "valor_anterior": row["valor_anterior"],
                    "valor_nuevo": row["valor_nuevo"],
                }
                registros_log.append(registro_log)
            return registros_log

        except Exception as ex:
            return {"error": f"No se puede obtener registro_logs_log desde el servicio: {str(ex)}"}
    
    @staticmethod
    def createRegistro_log_service(db, data):
        try:
            idRegistro = data.get("idRegistro")
            idUsuario = data.get("idUsuario")
            campo_modificado = data.get("campo_modificado")
            valor_anterior = data.get("valor_anterior")
            valor_nuevo = data.get("valor_nuevo")
            
            required_fields = {
                    "idRegistro": idRegistro,
                    "idUsuario": idUsuario,
                    "campo_modificado": campo_modificado,
                    "valor_anterior": valor_anterior,
                    "valor_nuevo": valor_nuevo,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            
            return Registro_logRepository.createRegistro_log(
                db, 
                idRegistro, 
                idUsuario, 
                campo_modificado, 
                valor_anterior, 
                valor_nuevo
            )
        
        except Exception as ex:
            return {"error": f"No se pudo crear el registro_log desde el servicio. {str(ex)}"}