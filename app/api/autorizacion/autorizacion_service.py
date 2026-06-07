from app.api.autorizacion.autorizacion_repository import AutorizacionRepository

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
                    "hora_salida": str(row["hora_salida"]) if row["hora_salida"] is not None else None, 
                    "hora_salida_digitada": str(row["hora_salida_digitada"]) if row["hora_salida_digitada"] is not None else None, 
                    "hora_salida_marcaje": str(row["hora_salida_marcaje"]) if row["hora_salida_marcaje"] is not None else None, 
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
                
                autorizacion["_saveStatus"] 

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
            
            required_fields = {
                    "idEmpleado": idEmpleado, 
                    "fecha": fecha, 
                    "horas_autorizadas": horas_autorizadas, 
                    "autorizado": autorizado, 
                    "observacion": observacion, 
                    "fecha_autorizacion": fecha_autorizacion, 
                    "usuario_autorizacion": usuario_autorizacion, 
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
            )
        
        except Exception as ex:
            return {"error": f"No se pudo crear el autorizacion. {ex}"}
        
    