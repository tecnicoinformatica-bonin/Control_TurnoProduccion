from app.api.registro_motivo_desasignacion.registro_motivo_desasignacion_repository import Registro_registro_motivo_desasignacionRepository
from app.extensions.slugify import Slugify

class Registro_motivo_desasignacion_Service():
    @staticmethod
    def get_count_motivos_desasignacion_service(db, from_date, to_date):
        try:
            data = Registro_registro_motivo_desasignacionRepository.get_count_motivos_desasignacion(db, from_date, to_date)
            registros_motivo_desasignacion = []
            for row in data:
                registro_motivo_desasignacion = {
                    "descripcion": row["descripcion"],
                    "conteo": row["conteo"],
                }
                registros_motivo_desasignacion.append(registro_motivo_desasignacion)

            encabezado = {
                "from_date": from_date,
                "to_date": to_date,
            }
            
            return (encabezado, registros_motivo_desasignacion)

        except Exception as ex:
            raise Exception(f"No se pudo obtener los datos en el servicio: {str(ex)}")
    
    @staticmethod
    def get_detalles_motivo_descripcion_service(db):
        try:
            data = Registro_registro_motivo_desasignacionRepository.get_detalles_motivo_descripcion(db)
            registros_motivo_desasignacion = []
            for row in data:
                registro_motivo_desasignacion = {
                    "idRegistro": row["idRegistro"],
                    "idMotivo": row["idMotivo"],
                    "descripcion": row["descripcion"],
                    "idEmpleado": row["idEmpleado"],
                    "badgeNumber": row["badgeNumber"],
                    "NombreEmpleado": row["NombreEmpleado"],
                }
                registros_motivo_desasignacion.append(registro_motivo_desasignacion)
            return registros_motivo_desasignacion

        except Exception as ex:
            return {"error": f"No se pudo obtener registros_registro_motivo_desasignacion en servicio: {str(ex)}"}
    
    @staticmethod
    def get_detalles_motivo_descripcion_by_idProgramacion_service(db, idProgramacion):
        try:
            data = Registro_registro_motivo_desasignacionRepository.get_detalles_motivo_descripcion_by_idProgramacion(db, idProgramacion)
            registros_motivo_desasignacion = []
            for row in data:
                registro_motivo_desasignacion = {
                    "idRegistro": row["idRegistro"],
                    "idMotivo": row["idMotivo"],
                    "descripcion": row["descripcion"],
                    "idEmpleado": row["idEmpleado"],
                    "badgeNumber": row["badgeNumber"],
                    "NombreEmpleado": row["NombreEmpleado"],
                }
                registros_motivo_desasignacion.append(registro_motivo_desasignacion)
            return registros_motivo_desasignacion

        except Exception as ex:
            return {"error": f"No se pudo obtener registros_registro_motivo_desasignacion en servicio: {str(ex)}"}
    
    @staticmethod
    def createRegistro_registro_motivo_desasignacion_service(db, data):
        try:
            idRegistro = data.get("idRegistro")
            idMotivo = data.get("idMotivo")
            
            required_fields = {
                "idRegistro": idRegistro, 
                "idMotivo": idMotivo, 
            }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {
                    "success": False,
                    "error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"
                    }
            
            result = Registro_registro_motivo_desasignacionRepository.create_registro_motivo_desasignacion(db, idRegistro, idMotivo)

            if "error" in result:
                return result

            return {
                "success": True,
                "mensaje": "Creado exitosamente",
                "creado": result
                }
        
        except Exception as ex:
            return {"error": f"No se pudo crear el registro_motivo_desasignacion en el servicio. {str(ex)}"}