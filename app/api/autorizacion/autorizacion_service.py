from datetime import datetime

import pytz

from app.api.autorizacion.autorizacion_repository import AutorizacionRepository
from app.api.departamento.departamento_service import Departamento_Service
from app.api.usuario.usuario_service import Usuario_Service

class Autorizacion_Service():
    @staticmethod
    def getAutorizaciones_service(db):
        try:
            data = AutorizacionRepository.getAutorizaciones(db)
            autorizaciones = []
            for row in data:
                autorizacion = {
                    "idAutorizacion": row["idAutorizacion"],
                    "idEmpleado": row["idEmpleado"],
                    "fecha": row["fecha"],
                    "horas_autorizadas": row["horas_autorizadas"],
                    "autorizado": row["autorizado"],
                    "observacion": row["observacion"],
                    "fecha_autorizacion": row["fecha_autorizacion"],
                    "usuario_autorizacion": row["usuario_autorizacion"],
                    "idRegistro": row["idRegistro"],
                }
                
                autorizaciones.append(autorizacion)
            return autorizaciones

        except Exception as ex:
            return {"error": f"No se pudo obtener autorizacion en el servicio: {str(ex)}"}
    
    @staticmethod
    def getAutorizacionesByEmpleado_service(db, idEmpleado):
        try:
            data = AutorizacionRepository.getAutorizacionByEmpleado(db, idEmpleado)
            autorizaciones = []
            for row in data:
                autorizacion = {
                    "idAutorizacion": row["idAutorizacion"],
                    "idEmpleado": row["idEmpleado"],
                    "fecha": row["fecha"],
                    "horas_autorizadas": row["horas_autorizadas"],
                    "autorizado": row["autorizado"],
                    "observacion": row["observacion"],
                    "fecha_autorizacion": row["fecha_autorizacion"],
                    "usuario_autorizacion": row["usuario_autorizacion"],
                    "idRegistro": row["idRegistro"],
                }
                autorizaciones.append(autorizacion)
            return autorizaciones

        except Exception as ex:
            return {"error": f"No se pudo obtener autorizacion en el servicio: {str(ex)}"}
   
    @staticmethod
    def getAutorizacionById_service(db, idAutorizacion):
        try:
            data = AutorizacionRepository.getAutorizacionById(db, idAutorizacion)
            autorizacion = {
                "idAutorizacion": data["idAutorizacion"],
                "idEmpleado": data["idEmpleado"],
                "fecha": data["fecha"],
                "horas_autorizadas": data["horas_autorizadas"],
                "autorizado": data["autorizado"],
                "observacion": data["observacion"],
                "fecha_autorizacion": data["fecha_autorizacion"],
                "usuario_autorizacion": data["usuario_autorizacion"],
                "idRegistro": data["idRegistro"],
            }

            return autorizacion

        except Exception as ex:
            return {"error": f"No se pudo obtener autorizacion en el servicio: {str(ex)}"}
    
    @staticmethod
    def get_detalles_autorizaciones_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_detalles_autorizaciones(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                fecha = row["fecha"].strftime("%Y-%m-%d")
                autorizacion = {
                    "idEmpleado": row["idEmpleado"], 
                    "idRegistro": row["idRegistro"], 
                    "nombre_completo": row["nombre_completo"], 
                    "fecha": fecha, 
                    "hora_entrada": str(row["hora_entrada"]) if row["hora_entrada"] is not None else None, 
                    "hora_entrada_digitada": str(row["hora_entrada_digitada"]) if row["hora_entrada_digitada"] is not None else None, 
                    "hora_entrada_marcaje": str(row["hora_entrada_marcaje"]) if row["hora_entrada_marcaje"] is not None else None, 
                    "hora_entrada_garita": str(row["hora_entrada_garita"]) if row["hora_entrada_garita"] is not None else None, 
                    "hora_salida": str(row["hora_salida"]) if row["hora_salida"] is not None else None, 
                    "hora_salida_digitada": str(row["hora_salida_digitada"]) if row["hora_salida_digitada"] is not None else None, 
                    "hora_salida_marcaje": str(row["hora_salida_marcaje"]) if row["hora_salida_marcaje"] is not None else None, 
                    "hora_salida_garita": str(row["hora_salida_garita"]) if row["hora_salida_garita"] is not None else None, 
                    "horas_temprano": row["horas_temprano"], 
                    "horas_tarde": row["horas_tarde"], 
                    "total_horas": row["total_horas"], 
                    "total_digitado": row["total_digitado"], 
                    "diferencia": row["diferencia"], 
                    "total_horas_autorizables": row["total_horas_autorizables"], 
                    "horas_autorizadas": row["horas_autorizadas"], 
                    "autorizado": row["autorizado"], 
                    "observacion": row["observacion"], 
                    "usuario_autorizacion": row["usuario_autorizacion"], 
                    "fecha_autorizacion": row["fecha_autorizacion"], 
                }

                if autorizacion["total_horas_autorizables"] is not None and autorizacion["horas_autorizadas"] is not None:
                    autorizacion["pendiente_de_autorizar"] = int(autorizacion["total_horas_autorizables"] - int(autorizacion["horas_autorizadas"]))
                if autorizacion["horas_autorizadas"] is None:
                    autorizacion["pendiente_de_autorizar"] = int(autorizacion["total_horas_autorizables"])

                if autorizacion["autorizado"] == 0 and autorizacion["usuario_autorizacion"] == None:
                    autorizacion["_saveStatus"] = "pending"
                if autorizacion["autorizado"] == 1 or autorizacion["autorizado"] == True: 
                    autorizacion["_saveStatus"] = "authorized"
                if (autorizacion["autorizado"] == 0 or autorizacion["autorizado"] == False) and autorizacion["usuario_autorizacion"] is not None: 
                    autorizacion["_saveStatus"] = "unauthorized"

                autorizacion["hora_entrada_reloj"] = autorizacion["hora_entrada_marcaje"] if autorizacion["hora_entrada_marcaje"] is not None else autorizacion["hora_entrada_garita"]
                autorizacion["hora_salida_reloj"] = autorizacion["hora_salida_marcaje"] if autorizacion["hora_salida_marcaje"] is not None else autorizacion["hora_salida_garita"]
                
                autorizaciones.append(autorizacion)

            return autorizaciones

        except Exception as ex:
            return {"error": f"No se pudo obtener autorizacion en el servicio: {str(ex)}"}
            
    @staticmethod
    def guardar_autorizacion_service(db, data):
        try:
            idEmpleado = data.get("idEmpleado")
            fecha = data.get("fecha")
            horas_autorizadas = data.get("horas_autorizadas")
            autorizado = data.get("autorizado")
            observacion = data.get("observacion")
            fecha_autorizacion = data.get("fecha_autorizacion")
            usuario_autorizacion = data.get("usuario_autorizacion")
            idRegistro = data.get("idRegistro")
            
            required_fields = {
                "idEmpleado": idEmpleado, 
                "fecha": fecha, 
                "horas_autorizadas": horas_autorizadas, 
                "autorizado": autorizado, 
                "observacion": observacion, 
                "fecha_autorizacion": fecha_autorizacion, 
                "usuario_autorizacion": usuario_autorizacion, 
                "idRegistro": idRegistro, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return AutorizacionRepository.guardar_autorizacion(
                db,
                idEmpleado,
                fecha,
                horas_autorizadas,
                autorizado,
                observacion,
                fecha_autorizacion,
                usuario_autorizacion,
                idRegistro
            )
        
        except Exception as ex:
            return {"error": f"No se pudo crear el autorizacion. {ex}"}
        

    def get_registros_con_horas_extra(db, fecha, idDeparment):
        try:
            data = Autorizacion_Service.get_detalles_autorizaciones_service(db, fecha, fecha, idDeparment)
            registros_autorizados = []
            for row in data:
                if(
                    row["total_horas"] > 0
                    and row["diferencia"] <= 0
                ):
                    registro = {
                        "idEmpleado": row["idEmpleado"],
                        "idRegistro": row["idRegistro"],
                        "nombre_completo": row["nombre_completo"],
                        "fecha": row["fecha"],
                        "hora_entrada": row["hora_entrada"],
                        "hora_entrada_digitada": row["hora_entrada_digitada"],
                        "hora_entrada_marcaje": row["hora_entrada_marcaje"],
                        "hora_salida": row["hora_salida"],
                        "hora_salida_digitada": row["hora_salida_digitada"],
                        "hora_salida_marcaje": row["hora_salida_marcaje"],
                        "horas_temprano": row["horas_temprano"],
                        "horas_tarde": row["horas_tarde"],
                        "total_horas": row["total_horas"],
                        "total_digitado": row["total_digitado"],
                        "diferencia": row["diferencia"],
                        "total_horas_autorizables": row["total_horas_autorizables"],
                        "horas_autorizadas": row["horas_autorizadas"],
                        "autorizado": row["autorizado"],
                        "observacion": row["observacion"],
                        "usuario_autorizacion": row["usuario_autorizacion"],
                        "fecha_autorizacion": row["fecha_autorizacion"],
                    }
                    
                    registros_autorizados.append(registro)

            return registros_autorizados

        except Exception as ex:
            return {"error": f"No se pudo obtener registros con horas extra y sin diferencia en el servicio: {str(ex)}"}

    @staticmethod
    def create_autorizacion_automatica(db, fecha, idDeparment):
        try:
            data = Autorizacion_Service.get_registros_con_horas_extra(db, fecha, idDeparment)
            tz = pytz.timezone("America/Guatemala")
            fecha_actual = datetime.now(tz)
            autorizaciones_realizadas = 0

            if data is None or data == []:
                return autorizaciones_realizadas            

            for row in data:
                dataRegistro = {
                    "idEmpleado": row["idEmpleado"], 
                    "fecha": fecha, 
                    "horas_autorizadas": row["total_horas"], 
                    "autorizado": 1, 
                    "observacion": "Autorizado automáticamente por el sistema", 
                    "fecha_autorizacion": fecha_actual, 
                    "usuario_autorizacion": 0, 
                    "idRegistro": row["idRegistro"]
                }
                Autorizacion_Service.guardar_autorizacion_service(db, dataRegistro)
                autorizaciones_realizadas += 1
            
            return autorizaciones_realizadas

        except Exception as ex:
            return {"error": f"No se pudo autorización automática en el servicio: {str(ex)}"}


    @staticmethod
    def get_detalles_autorizaciones_reporte_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_detalles_autorizaciones_reporte(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                fecha = row["fecha"].strftime("%Y-%m-%d")
                autorizacion = {
                    "badgeNumber": row["badgeNumber"], 
                    "idEmpleado": row["idEmpleado"], 
                    "idRegistro": row["idRegistro"], 
                    "nombre_completo": row["nombre_completo"], 
                    "fecha": fecha, 
                    "hora_entrada": str(row["hora_entrada"]) if row["hora_entrada"] is not None else None, 
                    "hora_entrada_digitada": str(row["hora_entrada_digitada"]) if row["hora_entrada_digitada"] is not None else None, 
                    "hora_entrada_marcaje": str(row["hora_entrada_marcaje"]) if row["hora_entrada_marcaje"] is not None else None, 
                    "hora_entrada_garita": str(row["hora_entrada_garita"]) if row["hora_entrada_garita"] is not None else None, 
                    "hora_salida": str(row["hora_salida"]) if row["hora_salida"] is not None else None, 
                    "hora_salida_digitada": str(row["hora_salida_digitada"]) if row["hora_salida_digitada"] is not None else None, 
                    "hora_salida_marcaje": str(row["hora_salida_marcaje"]) if row["hora_salida_marcaje"] is not None else None, 
                    "hora_salida_garita": str(row["hora_salida_garita"]) if row["hora_salida_garita"] is not None else None, 
                    "horas_temprano": row["horas_temprano"], 
                    "horas_tarde": row["horas_tarde"], 
                    "total_horas": row["total_horas"], 
                    "total_digitado": row["total_digitado"], 
                    "diferencia": row["diferencia"], 
                    "total_horas_autorizables": row["total_horas_autorizables"], 
                    "horas_autorizadas": row["horas_autorizadas"], 
                    "autorizado": row["autorizado"], 
                    "observacion": row["observacion"], 
                    "usuario_autorizacion": row["usuario_autorizacion"], 
                    "fecha_autorizacion": row["fecha_autorizacion"], 
                }

                if autorizacion["usuario_autorizacion"] is not None:
                    usuario = Usuario_Service.getUsuarioById_service(db, autorizacion["usuario_autorizacion"])
                else:
                    usuario = None

                autorizacion["nombreUsuario"] = usuario["nombre"] if usuario is not None else ""

                autorizacion["hora_entrada_reloj"] = autorizacion["hora_entrada_marcaje"] if autorizacion["hora_entrada_marcaje"] is not None else autorizacion["hora_entrada_garita"]
                autorizacion["hora_salida_reloj"] = autorizacion["hora_salida_marcaje"] if autorizacion["hora_salida_marcaje"] is not None else autorizacion["hora_salida_garita"]
                
                autorizaciones.append(autorizacion)

            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizaciones)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    @staticmethod
    def get_detalles_pendientes_reporte_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_detalles_pendientes_reporte(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                fecha = row["fecha"].strftime("%Y-%m-%d")
                autorizacion = {
                    "badgeNumber": row["badgeNumber"], 
                    "idEmpleado": row["idEmpleado"], 
                    "idRegistro": row["idRegistro"], 
                    "nombre_completo": row["nombre_completo"], 
                    "fecha": fecha, 
                    "diferencia": row["diferencia"], 
                }

                autorizaciones.append(autorizacion)
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizaciones)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    @staticmethod
    def get_resumen_horas_autorizadas_reporte_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_resumen_horas_autorizadas_reporte(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                autorizacion = {
                    "idEmpleado": row["idEmpleado"], 
                    "nombre_completo": row["nombre_completo"], 
                    "suma_horas_autorizadas": row["suma_horas_autorizadas"], 
                }

                autorizaciones.append(autorizacion)
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizaciones)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    @staticmethod
    def get_horas_autorizadas_por_empleado_linea_fecha_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_horas_autorizadas_por_empleado_linea_fecha(db, from_date, to_date, idDepartment)
            autorizaciones = {}
            
            for row in data:   

                idEmpleado = row["idEmpleado"]

                if idEmpleado not in autorizaciones:
                    autorizaciones[idEmpleado] = {
                        "idEmpleado": idEmpleado,
                        "nombre_completo": row["nombre_completo"],
                        "centro_de_costo": row["nombreCentro"],
                        "fechas": {}
                    } 

                autorizaciones[idEmpleado]["fechas"][row["fecha"].strftime("%Y-%m-%d")] = {
                    "horas": float(row["horas_autorizadas"]),
                    "linea": row["nameLinea"]
                }

            
            autorizacionesList = list(autorizaciones.values())
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizacionesList)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    @staticmethod
    def get_horas_autorizadas_por_empleado_linea_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_horas_autorizadas_por_empleado_linea(db, from_date, to_date, idDepartment)
            autorizaciones = {}
            
            for row in data:   

                idEmpleado = row["idEmpleado"]

                if idEmpleado not in autorizaciones:
                    autorizaciones[idEmpleado] = {
                        "idEmpleado": idEmpleado,
                        "nombre_completo": row["nombre_completo"],
                        "centro_de_costo": row["nombreCentro"],
                        "lineas": {}
                    } 

                autorizaciones[idEmpleado]["lineas"][row["nameLinea"]] = {
                    "linea": row["nameLinea"],
                    "horas": float(row["horas_autorizadas_linea"])
                }

            
            autorizacionesList = list(autorizaciones.values())
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "idDepartment": idDepartment,
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizacionesList)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    # Primera parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_centros_de_costo_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_resumen_horas_autorizadas_centros_de_costo(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                autorizacion = {
                    "nombreCentro": row["nombreCentro"],
                    "horas_centro_costo": row["horas_centro_costo"],
                    "horas_linea": row["horas_linea"],
                    "diferencia": row["diferencia"],
                }

                autorizaciones.append(autorizacion)
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "idDepartment": idDepartment,
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizaciones)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")

    # Segunda parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod        
    def get_resumen_horas_autorizadas_centros_asignados_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_resumen_horas_autorizadas_centros_asignados(db, from_date, to_date, idDepartment)
            autorizaciones = {}
            
            for row in data:   

                nombreCentro = row["nombreCentro"]

                if nombreCentro not in autorizaciones:
                    autorizaciones[nombreCentro] = {
                        "nombreCentro": row["nombreCentro"],
                        "lineas": {}
                    } 

                if row["nameLinea"] not in autorizaciones[nombreCentro]["lineas"]:
                    autorizaciones[nombreCentro]["lineas"][row["nameLinea"]] = {
                        "linea": row["nameLinea"],
                        "horas": float(row["horas_autorizadas_linea"])
                    }
                else:
                    autorizaciones[nombreCentro]["lineas"][row["nameLinea"]]["horas"] += float(row["horas_autorizadas_linea"])
            
            autorizacionesList = list(autorizaciones.values())
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "idDepartment": idDepartment,
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizacionesList)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
    
    # Segunda parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod        
    def get_resumen_horas_autorizadas_lineas_asignados_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_resumen_horas_autorizadas_lineas_asignados(db, from_date, to_date, idDepartment)
            autorizaciones = {}
            
            for row in data:   

                nameLinea = row["nameLinea"]

                if nameLinea not in autorizaciones:
                    autorizaciones[nameLinea] = {
                        "nameLinea": row["nameLinea"],
                        "centros": {}
                    } 

                if row["nombreCentro"] not in autorizaciones[nameLinea]["centros"]:
                    autorizaciones[nameLinea]["centros"][row["nombreCentro"]] = {
                        "centro": row["nombreCentro"],
                        "horas": float(row["horas_autorizadas_centro"])
                    }
                else:
                    autorizaciones[nameLinea]["centros"][row["nombreCentro"]]["horas"] += float(row["horas_autorizadas_centro"])
            
            autorizacionesList = list(autorizaciones.values())
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "idDepartment": idDepartment,
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizacionesList)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")
        
     # Cuarta parte del reporte resumen_horas_autorizadas_lineas_general.xlsm 
    @staticmethod
    def get_resumen_horas_autorizadas_lineas_service(db, from_date, to_date, idDepartment):
        try:
            data = AutorizacionRepository.get_resumen_horas_autorizadas_lineas(db, from_date, to_date, idDepartment)
            autorizaciones = []
            
            for row in data:   
                autorizacion = {
                    "nameLinea": row["nameLinea"],
                    "horas_autorizadas": row["horas_autorizadas"],
                }

                autorizaciones.append(autorizacion)
            
            departamento = Departamento_Service.getDepartamentoById_service(db, idDepartment)
            encabezado = {
                "idDepartment": idDepartment,
                "nombreDepartamento": departamento["name"],
                "from_date": from_date,
                "to_date": to_date,
            }

            return (encabezado, autorizaciones)

        except Exception as ex:
            raise Exception (f"No se pudo obtener autorizacion en el servicio: {str(ex)}")