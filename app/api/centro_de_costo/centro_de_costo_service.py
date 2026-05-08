from app.api.centro_de_costo.centro_de_costo_repository import Centro_de_costoRepository
from app.extensions.slugify import Slugify

class Centro_de_costo_Service():
    @staticmethod
    def getCentros_de_costo_service(db):
        try:
            data = Centro_de_costoRepository.getCentros_de_costo(db)
            centros_de_costo = []
            for row in data:
                centro_de_costo = {
                    "idCentro": row[0], 
                    "nombreCentro": row[1], 
                    "idDepartment": row[2], 
                }
                centros_de_costo.append(centro_de_costo)
            return centros_de_costo

        except Exception as ex:
            return {"mensaje": f"No se pudo obtener centros de costo en el servicio: {str(ex)}"}
            
    @staticmethod
    def getCentros_de_costoByDepartment_service(db, data):
        try:
            data = Centro_de_costoRepository.getCentro_de_costoByDepartment(db, data)
            centros_de_costo = []
            for row in data:
                centro_de_costo = {
                    "idCentro": row[0], 
                    "nombreCentro": row[1], 
                    "idDepartment": row[2], 
                }
                centros_de_costo.append(centro_de_costo)
                
            return centros_de_costo

        except Exception as ex:
            return {"mensaje": f"No se pudo obtener centros de costo en el servicio: {str(ex)}"}
            
    @staticmethod
    def createCentro_de_costo_service(db, data):
        try:
            nombreCentro = data.get("nombreCentro")
            idDepartment = data.get("idDepartment")
            
            required_fields = {
                    "nombreCentro": nombreCentro, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Centro_de_costoRepository.createCentro_de_costo(db, nombreCentro, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el centro de costo en el servicio: {str(ex)}"}
        
    @staticmethod
    def updateCentro_de_costo_service(db, data):
        try:
            idCentro = data.get("idCentro")
            nombreCentro = data.get("nombreCentro")
            idDepartment = data.get("idDepartment")

            required_fields = {
                    "idCentro": idCentro, 
                    "nombreCentro": nombreCentro, 
                    "idDepartment": idDepartment, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Centro_de_costoRepository.updateCentro_de_costo(db, idCentro, nombreCentro, idDepartment)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el centro de costo en el serivico: {str(ex)}"}
        
    @staticmethod
    def deleteCentro_de_costo_service(db, data):
        try:
            idCentro = data.get("idCentro")
            
            if not idCentro:
                return {"error": "ID de la línea es requerido."}
            
            return Centro_de_costoRepository.deleteCentro_de_costo(db, idCentro)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar el centro de costo en el servicio: {str(ex)}"}