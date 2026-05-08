from app.api.ruta.ruta_repository import RutaRepository

class Ruta_Service():
    @staticmethod
    def getRutas_service(db):
        try:
            data = RutaRepository.getRutas(db)
            rutas = []
            for row in data:
                ruta = {
                    "idRuta": row[0], 
                    "path": row[1], 
                }
                rutas.append(ruta)
            return rutas

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def getRutasDESC_service(db):
        try:
            data = RutaRepository.getRutasDESC(db)
            rutas = []
            for row in data:
                ruta = {
                    "idRuta": row[0], 
                    "path": row[1], 
                }
                rutas.append(ruta)
            return rutas

        except Exception as ex:
            raise Exception(ex)
            
    @staticmethod
    def createRuta_service(db, data):
        try:
            path = data.get("path")
            
            required_fields = {
                    "path": path, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return RutaRepository.createRuta(db, path)
        
        except Exception as ex:
            return {"error": f"No se pudo crear la ruta. {ex}"}
        
    @staticmethod
    def updateRuta_service(db, data):
        try:
            idRuta = data.get("idRuta")
            path = data.get("path")
            
            required_fields = {
                    "idRuta": idRuta, 
                    "path": path, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return RutaRepository.updateRuta(db, idRuta, path)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar la ruta. {ex}"}
        
    @staticmethod
    def deleteRuta_service(db, data):
        try:
            idRuta = data.get("idRuta")
            
            if not idRuta:
                return {"error": "ID de la ruta es requerido."}
            
            return RutaRepository.deleteRuta(db, idRuta)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la ruta. {ex}"}