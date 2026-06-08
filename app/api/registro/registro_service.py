from flask_login import current_user

from app.api.centro_de_costo.centro_de_costo_service import Centro_de_costo_Service
from app.api.empleado.empleado_service import Empleado_Service
from app.api.horario.horario_service import Horario_Service
from app.api.linea.linea_service import Linea_Service
from app.api.proceso.proceso_service import Proceso_Service
from app.api.programacion.programacion_service import Programacion_Service
from app.api.registro.registro_repository import RegistroRepository

import traceback
from app.api.registro_log.registro_log_service import Registro_log_Service
from app.api.usuario.usuario_service import Usuario_Service
from app.extensions.beneficios import calcular_beneficios
from app.extensions.calcular_diferencia_horas import calcular_diferencia_horas
from app.extensions.logs import compare_values_in_logs

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
                "cena_con_costo": data[14],
                "ultima_modificacion": data[15],
                "usuario_modificacion": data[16],
                "diferencia_horas": data[17],
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
                    "fecha": row[11],
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                    "cena_con_costo": row[14],
                    "ultima_modificacion": row[15],
                    "usuario_modificacion": row[16],
                    "diferencia_horas": row[17],
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
                    "hora_inicio": str(row[3]) if row[3] is not None else None,
                    "hora_fin": str(row[4]) if row[4] is not None else None,
                    "idLinea": row[5],
                    "idProceso": row[6],
                    "aplica_almuerzo": row[7],
                    "aplica_cena": row[8],
                    "aplica_transporte": row[9],
                    "observacion_transporte": row[10],
                    "fecha": row[11].isoformat(),
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                    "cena_con_costo": row[14],
                    "ultima_modificacion": str(row[15]) if row[15] else "",
                    "usuario_modificacion": row[16],
                    "diferencia_horas": row[17],
                }
                if(
                    registro["idLinea"] is None or
                    registro["idProceso"] is None or
                    registro["hora_inicio"] is None or
                    registro["hora_fin"] is None
                ):
                    registro["_saveStatus"] = "unassigned"
                else:
                    registro["_saveStatus"] = "saved"
                    
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
                    "idLinea": row[5],
                    "idProceso": row[6],
                    "aplica_almuerzo": row[7],
                    "aplica_cena": row[8],
                    "aplica_transporte": row[9],
                    "observacion_transporte": row[10],
                    "fecha": row[11].isoformat(),
                    "idCentro": row[12],
                    "badgeNumber": row[13],
                    "cena_con_costo": row[14],
                    "ultima_modificacion": row[15],
                    "usuario_modificacion": row[16],
                    "diferencia_horas": row[17],
                }
                
                if not registro["idLinea"] or not registro["idProceso"]:
                    continue

                hora_inicio = row[3]
                hora_fin = row[4]
                fecha = row[11]

                registro["hora_inicio"] = str(row[3]) if row[3] else None
                registro["hora_fin"] = str(row[4]) if row[4] else None

                beneficios = calcular_beneficios(
                    fecha,
                    hora_inicio,
                    hora_fin
                )

                registro["aplica_almuerzo"] = beneficios["aplica_almuerzo"]
                registro["aplica_cena"] = beneficios["aplica_cena"]
                registro["cena_con_costo"] = beneficios["cena_con_costo"]

                dataEmpleado = Empleado_Service.getEmpleadoById_service(db, registro["idEmpleado"])
                dataLinea = Linea_Service.getLineaById_service(db, registro["idLinea"])
                dataProceso = Proceso_Service.getProcesoById_service(db, registro["idProceso"])
                dataCentro = Centro_de_costo_Service.getCentros_de_costoById_service(db, registro["idCentro"])
                dataModificacion = RegistroRepository.getRegistroLastModification(db, registro["idProgramacion"])
                
                if registro["usuario_modificacion"]:
                    dataUsuario = Usuario_Service.getUsuarioById_service(db, registro["usuario_modificacion"])
                else:
                    dataUsuario = {
                        "nombre": None
                    }
                
                registro["nombreEmpleado"] = f"{dataEmpleado["firstName"]} {dataEmpleado["secondName"] or ""} {dataEmpleado["lastName"]} {dataEmpleado["lastName2"] or ""}"
                registro["nombreLinea"] = dataLinea["nameLinea"]
                registro["nombreProceso"] = dataProceso["proceso"]
                registro["nombreCentro"] = dataCentro["nombreCentro"]
                registro["nombre_usuario_modificacion"] = dataUsuario["nombre"] if dataUsuario["nombre"] is not None else "-----"
                registro["ultima_modificacion_programacion"] = dataModificacion["ultima_modificacion"]
                registro["nombreUsuarioModificacion_programacion"] = dataModificacion["nombreUsuarioModificacion"]

                print (f"{registro["nombre_usuario_modificacion"]} \n")
                registros.append(registro)
                # print("---------------------------")
                # print(f"idRegistro: {registro["idRegistro"]}")
                # print(f"idProgramacion: {registro["idProgramacion"]}")
                # print(f"idEmpleado: {registro["idEmpleado"]}")
                # print(f"idLinea: {registro["idLinea"]}")
                # print(f"idProceso: {registro["idProceso"]}")
                # print(f"aplica_almuerzo: {registro["aplica_almuerzo"]}")
                # print(f"aplica_cena: {registro["aplica_cena"]}")
                # print(f"aplica_transporte: {registro["aplica_transporte"]}")
                # print(f"observacion_transporte: {registro["observacion_transporte"]}")
                # print(f"fecha: {registro["fecha"]}")
                # print(f"idCentro: {registro["idCentro"]}")
                # print(f"badgeNumber: {registro["badgeNumber"]}")
                # print(f"cena_con_costo: {registro["cena_con_costo"]}")
                # print(f"aplica_almuerzo: {registro["aplica_almuerzo"]}")
                # print(f"aplica_cena: {registro["aplica_cena"]}")
                # print(f"cena_con_costo: {registro["cena_con_costo"]}")
                # print(f"nombreEmpleado: {registro["nombreEmpleado"]}")
                # print(f"nombreLinea: {registro["nombreLinea"]}")
                # print(f"nombreProceso: {registro["nombreProceso"]}")
                # print(f"nombreCentro: {registro["nombreCentro"]}")
                # print(f"nombreUsuarioModificaion: {registro["nombreUsuarioModificacion"]}")
            return registros

        except Exception as ex:
            traceback.print_exc()

            return {
                "error": f"No se puede obtener registros desde el servicio: {str(ex)}"
            }
        
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
            idRegistro = data.get("idRegistro")
            idProgramacion = data.get("idProgramacion")
            idEmpleado = data.get("idEmpleado")
            hora_inicio = data.get("hora_inicio")
            hora_fin = data.get("hora_fin")
            idLinea = data.get("idLinea")
            idProceso = data.get("idProceso")
            aplica_almuerzo = data.get("aplica_almuerzo")
            aplica_cena = data.get("aplica_cena")
            cena_con_costo = data.get("cena_con_costo")
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
                    # "cena_con_costo": aplica_cena,
                    # "aplica_transporte": aplica_transporte,
                    # "observacion_transporte": observacion_transporte,
                    # "fecha": fecha,
                    # "idCentro": idCentro,
                    # "badgeNumber": badgeNumber,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            beneficios = calcular_beneficios(
                fecha,
                hora_inicio,
                hora_fin
            )

            aplica_almuerzo = beneficios["aplica_almuerzo"]
            aplica_cena = beneficios["aplica_cena"]
            cena_con_costo = beneficios["cena_con_costo"]
            
            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, idProgramacion)

            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }

            return RegistroRepository.createRegistro(db,idRegistro, idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber, cena_con_costo)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el registro desde el servicio. {str(ex)}"}
        
    @staticmethod
    def createRegistroAutomatico_service(db, data):
        try:
            idProgramacion = data.get("idProgramacion")
            fecha = data.get("fecha")
            idCentro = data.get("idCentro")
            badgeNumber = data.get("badgeNumber")

            required_fields = {
                "idProgramacion": idProgramacion,
                "fecha": fecha,
                "idCentro": idCentro,
                "badgeNumber": badgeNumber,
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, idProgramacion)

            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }
            
            idDepartment = programacion["idDepartment"]
            
            empleados = Empleado_Service.getActiveEmpleadosByDepartment_service(db, idDepartment)
            return 
        
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
            }            
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            beneficios = calcular_beneficios(
                fecha,
                hora_inicio,
                hora_fin
            )

            aplica_almuerzo = beneficios["aplica_almuerzo"]
            aplica_cena = beneficios["aplica_cena"]
            cena_con_costo = beneficios["cena_con_costo"]

            # Horas extra calculadas
            empleado = Empleado_Service.getEmpleadoById_service(db, idEmpleado)
            horarioEmpleado = Horario_Service.getHorarioById_service(db, empleado["idHorario"])

            diferencia_horas = calcular_diferencia_horas(
                fecha,
                horarioEmpleado["hora_inicio"],
                horarioEmpleado["hora_fin"],
                hora_inicio, 
                hora_fin
            )
                                    
            datos_nuevos = {
                "idEmpleado": idEmpleado, 
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
            }

            registro = RegistroRepository.getRegistroById(db, idRegistro)
            registro_actual = Registro_Service.getRegistroById_service(db, idRegistro)
            logs = compare_values_in_logs(registro_actual, datos_nuevos)
            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro[1])
            
            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }
            
            dataUpdated = RegistroRepository.updateRegistro(
                db, 
                idRegistro, 
                idEmpleado, 
                hora_inicio, 
                hora_fin, 
                idLinea, 
                idProceso, 
                aplica_almuerzo, 
                aplica_cena, 
                aplica_transporte, 
                observacion_transporte, 
                fecha, 
                idCentro, 
                badgeNumber, 
                cena_con_costo, 
                diferencia_horas)
            
            for log in logs:
                data = {
                    "idRegistro": idRegistro,
                    "idUsuario": current_user.id,
                    "campo_modificado": log["campo"],
                    "valor_anterior": str(log["anterior"]),
                    "valor_nuevo": str(log["nuevo"])
                }
                log_insertado = Registro_log_Service.createRegistro_log_service(db, data)

            return {
                "success": True,
                "idRegistro": idRegistro,
                "aplica_almuerzo": aplica_almuerzo,
                "aplica_cena": aplica_cena,
                "cena_con_costo": cena_con_costo,
                "idEmpleado": idEmpleado,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
                "aplica_transporte": aplica_transporte,
                "observacion_transporte": observacion_transporte,
                "fecha": fecha,
                "idCentro": idCentro,
                "badgeNumber": badgeNumber,
                "diferencia_horas": diferencia_horas,
                "ultima_modificacion": dataUpdated["ultima_modificacion"],
                "usuario_modificacion": dataUpdated["usuario_modificacion"],
            }
        
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
    
    @staticmethod
    def updateRegistroToNulls_service(db, data):
        try:
            idRegistro = data.get("idRegistro")
            idEmpleado = data.get("idEmpleado")
            hora_inicio = None
            hora_fin = None
            idLinea = None
            idProceso = None
            aplica_transporte = 0
            observacion_transporte = ""
            fecha = data.get("fecha")
            idCentro = data.get("idCentro")
            badgeNumber = data.get("badgeNumber")
            diferencia_horas = None
            
            aplica_almuerzo = 0
            aplica_cena = 0
            cena_con_costo = 0
                                    
            datos_nuevos = {
                "idEmpleado": idEmpleado, 
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
                "aplica_transporte": aplica_transporte,
                "observacion_transporte": observacion_transporte,
                "aplica_almuerzo": aplica_almuerzo,
                "aplica_cena": aplica_cena,
                "cena_con_costo": cena_con_costo,
            }

            registro = RegistroRepository.getRegistroById(db, idRegistro)
            registro_actual = Registro_Service.getRegistroById_service(db, idRegistro)
            logs = compare_values_in_logs(registro_actual, datos_nuevos)
            programacion = Programacion_Service.getProgramacionByIdProgramacion_service(db, registro[1])
            
            if programacion["estado"] == "CERRADO":
                return { "error": "La programación ya se encuentra cerrada." }
            
            dataUpdated = RegistroRepository.updateRegistro(db, idRegistro, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber, cena_con_costo, diferencia_horas)
            
            for log in logs:
                data = {
                    "idRegistro": idRegistro,
                    "idUsuario": current_user.id,
                    "campo_modificado": log["campo"],
                    "valor_anterior": str(log["anterior"]),
                    "valor_nuevo": str(log["nuevo"])
                }
                log_insertado = Registro_log_Service.createRegistro_log_service(db, data)

            return {
                "success": True,
                "idRegistro": idRegistro,
                "aplica_almuerzo": aplica_almuerzo,
                "aplica_cena": aplica_cena,
                "cena_con_costo": cena_con_costo,
                "idEmpleado": idEmpleado,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "idLinea": idLinea,
                "idProceso": idProceso,
                "aplica_transporte": aplica_transporte,
                "observacion_transporte": observacion_transporte,
                "fecha": fecha,
                "idCentro": idCentro,
                "badgeNumber": badgeNumber,
                "ultima_modificacion": dataUpdated["ultima_modificacion"],
                "usuario_modificacion": dataUpdated["usuario_modificacion"],
            }
        
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