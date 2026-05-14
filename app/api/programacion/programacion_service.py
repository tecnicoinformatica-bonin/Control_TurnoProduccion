from datetime import datetime

from app.api.departamento.departamento_service import Departamento_Service
from app.api.programacion.programacion_repository import ProgramacionRepository
from app.api.usuario.usuario_service import Usuario_Service
from app.extensions.slugify import Slugify

class Programacion_Service():
    @staticmethod
    def getProgramaciones_service(db):
        try:
            data = ProgramacionRepository.getProgramaciones(db)
            programaciones = []
            for row in data:
                programacion = {
                    "idProgramacion": row[0], 
                    "fecha": row[1], 
                    "idDepartment": row[2],
                    "elaborado_por": row[3], 
                    "fecha_creacion": row[4], 
                    "estado": row[5], 
                    "fecha_cierre": row[6],
                    "cerrado_por": row[7], 
                    "fecha_reapertura": row[8],
                    "reabierto_por": row[9],
                    "motivo_reapertura": row[10],                }
                programaciones.append(programacion)
            return programaciones

        except Exception as ex:
            return {"error": f"No se pudieron obtener las programaciones en el servicio: {str(ex)}"}
    
    @staticmethod
    def getProgramacionByDateAndIdDepartment_service(db, fecha, idDepartment):
        try:
            data = ProgramacionRepository.getProgramacionByDateAndIdDepartment(db, fecha, idDepartment)
            programacion = {
                "idProgramacion": data[0], 
                "fecha": data[1], 
                "idDepartment": data[2],
                "elaborado_por": data[3], 
                "fecha_creacion": data[4], 
                "estado": data[5], 
                "fecha_cierre": data[6],
                "cerrado_por": data[7], 
                "fecha_reapertura": data[8],
                "reabierto_por": data[9],
                "motivo_reapertura": data[10],  
            }

            return programacion

        except Exception as ex:
            return {"error": f"No se pudieron obtener las programaciones en el servicio: {str(ex)}"}
    
    @staticmethod
    def getProgramacionByIdProgramacion_service(db, idProgramacion):
        try:
            data = ProgramacionRepository.getProgramacionById(db, idProgramacion)
            programacion = {
                "idProgramacion": data[0], 
                "fecha": data[1], 
                "idDepartment": data[2],
                "elaborado_por": data[3], 
                "fecha_creacion": data[4], 
                "estado": data[5], 
                "fecha_cierre": data[6],
                "cerrado_por": data[7], 
                "fecha_reapertura": data[8],
                "reabierto_por": data[9],
                "motivo_reapertura": data[10],  
            }

            return programacion

        except Exception as ex:
            return {"error": f"No se pudieron obtener las programaciones en el servicio: {str(ex)}"}
    
    @staticmethod
    def getDetallesProgramacionByIdProgramacion_service(db, idProgramacion):
        try:
            dataProgramacion = ProgramacionRepository.getProgramacionById(db, idProgramacion)
            dataDepartamento = Departamento_Service.getDepartamentos_service(db)
            dataUsuario = Usuario_Service.getUsuarios_service(db)

            programacion = {
                "idProgramacion": dataProgramacion[0], 
                "fecha": dataProgramacion[1], 
                "idDepartment": dataProgramacion[2],
                "elaborado_por": dataProgramacion[3], 
                "fecha_creacion": dataProgramacion[4], 
                "estado": dataProgramacion[5], 
                "fecha_cierre": dataProgramacion[6],
                "cerrado_por": dataProgramacion[7], 
                "fecha_reapertura": dataProgramacion[8],
                "reabierto_por": dataProgramacion[9],
                "motivo_reapertura": dataProgramacion[10],  
            }

            for row in dataDepartamento:
                if row["idDepartment"] == programacion["idDepartment"]:
                    programacion["nombreDepartamento"] = row["name"]

            for row in dataUsuario:
                if row["idUsuario"] == programacion["elaborado_por"]:
                    programacion["nombre_elaborado_por"] = row["nombre"]

                if row["idUsuario"] == programacion["cerrado_por"]:
                    programacion["nombre_cerrado_por"] = row["nombre"]

                if row["idUsuario"] == programacion["reabierto_por"]:
                    programacion["nombre_reabierto_por"] = row["nombre"]

            return programacion

        except Exception as ex:
            return {"error": f"No se pudieron obtener las programaciones en el servicio: {str(ex)}"}
    
    @staticmethod
    def getProgramacionesEnBorrador_service(db):
        try:
            data = ProgramacionRepository.getProgramacionesEnBorrador(db)
            programaciones = []
            for row in data:
                programacion = {
                    "idProgramacion": row[0], 
                    "fecha": row[1], 
                    "idDepartment": row[2],
                    "elaborado_por": row[3], 
                    "fecha_creacion": row[4], 
                    "estado": row[5], 
                    "fecha_cierre": row[6],
                    "cerrado_por": row[7], 
                    "fecha_reapertura": row[8],
                    "reabierto_por": row[9],
                    "motivo_reapertura": row[10],      
                }
                programaciones.append(programacion)
            return programaciones

        except Exception as ex:
            return {"error": f"No se pudieron obtener las programaciones en BORRADOR desde el servicio: {str(ex)}"}
            
    @staticmethod
    def createProgramacion_service(db, data):
        try:
            fecha = data.get("fecha")
            idDepartment = data.get("idDepartment")
            fecha_creacion = datetime.now()
            estado = "BORRADOR"

            required_fields = {
                    "fecha": fecha, 
                    "idDepartment": idDepartment,
                    "fecha_creacion": fecha_creacion, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProgramacionRepository.createProgramacion(db, fecha, idDepartment, fecha_creacion, estado)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el programacion. {str(ex)}"}
    
    @staticmethod
    def createProgramacionAutomatica_service(db, data):
        try:
            fecha = data.get("fecha")
            estado = "BORRADOR"
            current_time = datetime.now().date()
            departamentos_aplica_horas_extra = Departamento_Service.getDepartamentos_aplica_horas_extra_service(db)

            required_fields = {
                    "fecha": fecha,  
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}

            for depto in departamentos_aplica_horas_extra:
                existsProgramacion = ProgramacionRepository.getProgramacionByDateAndIdDepartment(db, fecha, depto['idDepartment'])

                if existsProgramacion:
                    continue

                ProgramacionRepository.createProgramacion(db, fecha, depto['idDepartment'], current_time, estado)

            return {"mensaje": "Reportes creados correctamente."}
            
        except Exception as ex:
            return {"error": f"No se pudo crear la programación. {str(ex)}"}
        
    @staticmethod
    def cerrarProgramacion_service(db, data):
        try:

            idProgramacion = data.get("idProgramacion")
            elaborado_por = data.get("elaborado_por")
            estado = "CERRADO"
            fecha_cierre = datetime.now()
            cerrado_por = data.get("cerrado_por")

            required_fields = {
                    "idProgramacion": idProgramacion, 
                    "elaborado_por": elaborado_por,
                    "estado": estado,
                    "fecha_cierre": fecha_cierre,
                    "cerrado_por": cerrado_por,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProgramacionRepository.cerrarProgramacion(db, idProgramacion, elaborado_por, estado, fecha_cierre, cerrado_por)
        
        except Exception as ex:
            return {"error": f"No se pudo cerrar la programación. {str(ex)}"}
        
    @staticmethod
    def cerrarProgramacionById_service(db, data):
        try:

            fecha = data.get("fecha")
            idDepartment = data.get("idDepartment")
            elaborado_por = data.get("elaborado_por")
            estado = "CERRADO"
            fecha_cierre = datetime.now()
            cerrado_por = data.get("cerrado_por")

            required_fields = {
                    "fecha": fecha, 
                    "idDepartment": idDepartment,
                    "elaborado_por": elaborado_por,
                    "estado": estado,
                    "fecha_cierre": fecha_cierre,
                    "cerrado_por": cerrado_por,
                }
                        
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProgramacionRepository.cerrarProgramacion(db, fecha, idDepartment, elaborado_por, estado, fecha_cierre, cerrado_por)
        
        except Exception as ex:
            return {"error": f"No se pudo cerrar la programación. {str(ex)}"}
        
    @staticmethod
    def reOpenProgramacion_service(db, data):
        try:

            fecha = data.get("fecha")
            idDepartment = data.get("idDepartment")
            estado = "BORRADOR"
            fecha_reapertura = datetime.now()
            reabierto_por = data.get("reabierto_por")
            motivo_reapertura = data.get("motivo_reapertura")

            required_fields = {
                    "fecha": fecha, 
                    "idDepartment": idDepartment,
                    "estado": estado,
                    "fecha_reapertura": fecha_reapertura,
                    "reabierto_por": reabierto_por,
                    "motivo_reapertura": motivo_reapertura,
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return ProgramacionRepository.reOpenProgramacion(db, fecha, idDepartment, estado, fecha_reapertura, reabierto_por, motivo_reapertura)
        
        except Exception as ex:
            return {"error": f"No se pudo reabrir la programación en el servicio: {str(ex)}"}
        
    @staticmethod
    def deleteProgramacion_service(db, data):
        try:
            idProgramacion = data.get("idProgramacion")
            
            if not idProgramacion:
                return {"error": "ID del programacion es requerido."}
            
            return ProgramacionRepository.deleteProgramacion(db, idProgramacion)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el programacion. {str(ex)}"}
        

    @staticmethod
    def cerrar_programaciones_vencidas_service(db):
        return ProgramacionRepository.cerrar_programaciones_vencidas(db)