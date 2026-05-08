from app.api.rol_ruta.rol_ruta_repository import Rol_Ruta_Repository

class Rol_Ruta_Service():
    @staticmethod
    def getRol_Rutas_service(db):
        try:
            data = Rol_Ruta_Repository.getRol_Rutas(db)
            rol_rutas = []
            for row in data:
                rol_ruta = {
                    "idRol": row[0], 
                    "idRuta": row[1], 
                }
                rol_rutas.append(rol_ruta)
            return rol_rutas

        except Exception as ex:
            return {"error": f"No se pudo obtener rol_rutas. {ex}"}
            
    @staticmethod
    def createRol_Ruta_service(db, data):
        try:
            idRol = data.get("idRol")
            idRuta = data.get("idRuta")
            
            required_fields = {
                    "idRol": idRol, 
                    "idRuta": idRuta, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Rol_Ruta_Repository.createRol_Ruta(db, idRol, idRuta)
        
        except Exception as ex:
            return {"error": f"No se pudo crear el rol_ruta. {ex}"}
        
    @staticmethod
    def updateRol_Ruta_service(db, data):
        try:
            idRol = data.get("idRol")
            idRuta = data.get("idRuta")
            
            required_fields = {
                    "idRol": idRol, 
                    "idRuta": idRuta, 
                }
            
            missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

            if missing_fields:
                return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
            
            return Rol_Ruta_Repository.updateRol_Ruta(db, idRol, idRuta)
        
        except Exception as ex:
            return {"error": f"No se pudo modificar el rol_ruta. {ex}"}
        
    @staticmethod
    def deleteRol_Ruta_service(db, data):
        try:
            idRol = data.get("idRol")
            idRuta = data.get("idRuta")
            
            if not idRol or not idRuta:
                return {"error": "ID de roll e ID de ruta de la rol_ruta son requeridos."}
            
            return Rol_Ruta_Repository.deleteRol_Ruta(db, idRol, idRuta)
        
        except Exception as ex:
            return {"error": f"No se pudo eliminar la rol_ruta. {ex}"}