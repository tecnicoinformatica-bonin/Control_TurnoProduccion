from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.linea.linea_service import Linea_Service
from app.api.proceso.proceso_service import Proceso_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro.registro_repository import RegistroRepository

class Registro_Service():
    @staticmethod
    def getRegistroById_service(db, id):
        try:
            data = RegistroRepository.getRegistroById(db, id)
            
            registro = {
                "idRegistro": data[0],
                "idProgramacion": data[1],
                "idEmpleado": data[2],
                "hora_inicio": data[3],
                "hora_fin": data[4],
                "idLinea": data[5],
                "idProceso": data[6],
                "aplica_almuerzo": data[7],
                "aplica_cena": data[8],
                "aplica_transporte": data[9],
                "observacion_transporte": data[10],
                "fecha": data[11].isoformat(),
                "idCentro": data[12],
                "badgeNumber": data[13],
            }
            
            return registro

        except Exception as ex:
            return {"error": f"No se puede obtener registros desde el servicio: {str(ex)}"}
        
    @staticmethod
    def getRegistros_service(db):
        try:
            data = RegistroRepository.getRegistros(db)
            registros = []
            for row in data:
                registro = {
                    "idRegistro": row[0],
                    "idProgramacion": row[1],
                    "idEmpleado": row[2],
                    "hora_inicio": str(row[3]) if row[3] else None,
                    "hora_fin": str(row[4]) if row[4] else None,
                    "idLinea": row[5],
                    "idProceso": row[6],
                    "aplica_almuerzo": row[7],
                    "aplica_cena": row[8],
                    "aplica_transporte": row[9],
                    "observacion_transporte": row[10],
                    "fecha": row[11].isoformat(),
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                }
                registros.append(registro)
            return registros

        except Exception as ex:
            return {"error": f"No se puede obtener registros desde el servicio: {str(ex)}"}
            
    @staticmethod
    def getRegistrosByProgramacion_service(db, idProgramacion):
        try:
            data = RegistroRepository.getRegistrosByProgramacion(db, idProgramacion)
            registros = []
            for row in data:
                registro = {
                    "idRegistro": row[0],
                    "idProgramacion": row[1],
                    "idEmpleado": row[2],
                    "hora_inicio": str(row[3]) if row[3] else None,
                    "hora_fin": str(row[4]) if row[4] else None,
                    "idLinea": row[5],
                    "idProceso": row[6],
                    "aplica_almuerzo": row[7],
                    "aplica_cena": row[8],
                    "aplica_transporte": row[9],
                    "observacion_transporte": row[10],
                    "fecha": row[11].isoformat(),
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                }
                registros.append(registro)
            return registros

        except Exception as ex:
            return {"error": f"No se puede obtener registros desde el servicio: {str(ex)}"}
    
    @staticmethod
    def getDetalleRegistrosByProgramacion_service(db, idProgramacion):
        try:
            dataRegistro = RegistroRepository.getRegistrosByProgramacion(db, idProgramacion)
                        
            registros = []
            for row in dataRegistro:
                registro = {
                    "idRegistro": row[0],
                    "idProgramacion": row[1],
                    "idEmpleado": row[2],
                    "hora_inicio": str(row[3]) if row[3] else None,
                    "hora_fin": str(row[4]) if row[4] else None,
                    "idLinea": row[5],
                    "idProceso": row[6],
                    "aplica_almuerzo": row[7],
                    "aplica_cena": row[8],
                    "aplica_transporte": row[9],
                    "observacion_transporte": row[10],
                    "fecha": row[11].isoformat(),
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                }

                dataEmpleado = Empleado_Service.getEmpleadoById_service(db, registro["idEmpleado"])
                dataLinea = Linea_Service.getLineaById_service(db, registro["idLinea"])
                dataProceso = Proceso_Service.getProcesoById_service(db, registro["idProceso"])
                dataCentro = Centro_de_costo_Service.getCentros_de_costoById_service(db, registro["idCentro"])
                
                registro["nombreEmpleado"] = f"{dataEmpleado["firstName"]} {dataEmpleado["secondName"] or ""} {dataEmpleado["lastName"]} {dataEmpleado["lastName2"] or ""}"
                registro["nombreLinea"] = dataLinea["nameLinea"]
                registro["nombreProceso"] = dataProceso["proceso"]
                registro["nombreCentro"] = dataCentro["nombreCentro"]

                registros.append(registro)
            return registros

        except Exception as ex:
            return {"error": f"No se puede obtener registros desde el servicio: {str(ex)}"}
        
    @staticmethod
    def getCount_aplica_cena_porProgramacion_service(db, idProgramacion):
        try:
            conteo = RegistroRepository.getCount_aplica_cena_porProgramacion(db, idProgramacion)

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede obtener conteo de cenas sin costo desde el servicio: {str(ex)}"}
            
    @staticmethod
    def getCount_no_aplica_cena_porProgramacion_service(db, idProgramacion):
        try:
            conteo = RegistroRepository.getCount_no_aplica_cena_porProgramacion(db, idProgramacion)

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede obtener conteo de cenas con costo desde el servicio: {str(ex)}"}
            
    @staticmethod
    def getCount_aplica_almuerzo_porProgramacion_service(db, idProgramacion):
        try:
            conteo = RegistroRepository.getCount_aplica_almuerzo_porProgramacion(db, idProgramacion)

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede obtener conteo de almuerzos sin costo desde el servicio: {str(ex)}"}

    @staticmethod
    def getCount_aplica_transporte_porProgramacion_service(db, idProgramacion):
        try:
            conteo = RegistroRepository.getCount_aplica_transporte_porProgramacion(db, idProgramacion)

            return conteo
        
        except Exception as ex:
            return {"error": f"No se puede obtener conteo de transporte que sí aplica, desde el servicio: {str(ex)}"}
            
    @staticmethod
    def createRegistro_service(db, data):
        try:
            idProgramacion = data.get("idProgramacion")
            idEmpleado = data.get("idEmpleado")
            hora_inicio = data.get("hora_inicio")
            hora_fin = data.get("hora_fin")
            idLinea = data.get("idLinea")
            idProceso = data.get("idProceso")
            aplica_almuerzo = data.get("aplica_almuerzo")
            aplica_cena = data.get("aplica_cena")
            aplica_transporte = data.get("aplica_transporte")
            observacion_transporte = data.get("observacion_transporte")
            fecha = data.get("fecha")
            idCentro = data.get("idCentro")
            badgeNumber = data.get("badgeNumber")

            required_fields = {
                    "idProgramacion": idProgramacion,
                    "idEmpleado": idEmpleado,
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "idLinea": idLinea,
                    "idProceso": idProceso,
                    # "aplica_almuerzo": aplica_almuerzo,
                    # "aplica_cena": aplica_cena,
                    # "aplica_transporte": aplica_transporte,
                    # "observacion_transporte": observacion_transporte,
                    # "fecha": fecha,
                    # "idCentro": idCentro,
                    # "badgeNumber": badgeNumber,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, idProgramacion)

            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }


            return RegistroRepository.createRegistro(db, idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el registro desde el servicio. {str(ex)}"}
        
    @staticmethod
    def updateRegistro_service(db, data):
        try:
            idRegistro = data.get("idRegistro")
            idEmpleado = data.get("idEmpleado")
            hora_inicio = data.get("hora_inicio")
            hora_fin = data.get("hora_fin")
            idLinea = data.get("idLinea")
            idProceso = data.get("idProceso")
            aplica_almuerzo = data.get("aplica_almuerzo")
            aplica_cena = data.get("aplica_cena")
            aplica_transporte = data.get("aplica_transporte")
            observacion_transporte = data.get("observacion_transporte")
            fecha = data.get("fecha")
            idCentro = data.get("idCentro")
            badgeNumber = data.get("badgeNumber")

            required_fields = {
                    "idRegistro": idRegistro, 
                    "idEmpleado": idEmpleado, 
                    "hora_inicio": hora_inicio,
                    "hora_fin": hora_fin,
                    "idLinea": idLinea,
                    "idProceso": idProceso,
                    # "aplica_almuerzo": aplica_almuerzo,
                    # "aplica_cena": aplica_cena,
                    # "aplica_transporte": aplica_transporte,
                    
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            registro = RegistroRepository.getRegistroById(db, idRegistro)

            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro[1])

            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }
            
            return RegistroRepository.updateRegistro(db, idRegistro, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el registro desde el servicio. {str(ex)}"}
        
    @staticmethod
    def deleteRegistro_service(db, data):
        try:
            idRegistro = data.get("idRegistro")

            if not idRegistro:
                return {"error": "ID del registro es requerido."}
            
            registro = RegistroRepository.getRegistroById(db, idRegistro)

            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro[1])

            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }
            
            
            return RegistroRepository.deleteRegistro(db, idRegistro)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el registro desde el servicio. {str(ex)}"}