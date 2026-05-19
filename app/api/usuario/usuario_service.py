from datetime import datetime

from flask import session
from werkzeug.security import check_password_hash
from flask_login import login_user

from app.api.usuario.usuario_repository import UsuarioRepository
from app.api.usuario.usuario_model import Usuario_Rutas

class Usuario_Service():
   @staticmethod
   def getUsuarios_service(db):
      try:
         data = UsuarioRepository.getUsuarios(db)
         usuarios = []
         for row in data:
            usuario =  {
               "idUsuario": row[0],
               "username": row[1],
               "nombre": row[2],
               "activo": row[4],               
            }
            usuarios.append(usuario)

         return usuarios
      except Exception as ex:
         return {"error": f"No se puede listar los usuarios. {ex}"}
      
   @staticmethod
   def createUsuario_service(db, data):
      try:
         username = data.get("username")
         nombre = data.get("nombre")
         password = data.get("password")
         activo = bool(data.get("activo"))
         
         if not username or not password:
            return {"error": "Nombre de usuario y contraseña son obligatorios"}, 400
         
         return UsuarioRepository.createUsuario(db, username, nombre, password, activo)
         
      except Exception as ex:
         return {"error": f"No se pudo crear el usuario. {ex}"}

   @staticmethod
   def updateUsuario_service(db, data):
      try:
         idUsuario = data.get("idUsuario")
         nombre = data.get("nombre")
         activo = bool(data.get("activo"))
         
         required_fields = {
                  "idUsuario": idUsuario, 
                  "nombre": nombre,
                  "activo": activo,
               }
         
         missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

         if missing_fields:
               return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
         
         return UsuarioRepository.updateUsuario(db, idUsuario, nombre, activo)
      
      except Exception as ex:
         return {"error": f"No se pudo modificar la usuario. {ex}"}
      
   @staticmethod
   def updatePassword_service(db, data):
      try:
         idUsuario = data.get("idUsuario")
         password = data.get("password")
         confirmedPassword = data.get("confirmedPassword")
         
         required_fields = {
                  "idUsuario": idUsuario, 
                  "password": password, 
                  "confirmedPassword": confirmedPassword, 
               }
         
         missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

         if missing_fields:
               return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
         
         if password != confirmedPassword:
            return {"error": f"Las contraseñas no son iguales."}
         
         return UsuarioRepository.updatePassword(db, idUsuario, password)
      
      except Exception as ex:
         return {"error": f"No se pudo modificar la contraseña. {ex}"}
      
   @staticmethod
   def deleteUsuario_service(db, data):
      try:
         idUsuario = data.get("idUsuario")
         
         if not idUsuario:
               return {"error": "ID de la usuario es requerido."}
         
         return UsuarioRepository.deleteUsuario(db, idUsuario)
      
      except Exception as ex:
         return {"error": f"No se pudo eliminar la usuario. {ex}"}   

   @staticmethod
   def login_service(db, data):
      username = data.get("username")
      password = data.get("password")

      if not username or not password:
         return {"error": "Usuario y contraseña requeridos", "status": 400}
         
      usuario = UsuarioRepository.getUsuarioByUsername(db, username)

      if not usuario:
         return {"error": f"Usuario {username} no existe", "status": 404}
         
      paths_usuario = UsuarioRepository.getUserPaths(db, usuario[0])
      permisos = UsuarioRepository.getUserPermissionsById(db, usuario[0])
      roles_usuario = UsuarioRepository.getUserRolesById(db, usuario[0])
      departamentos = UsuarioRepository.getUserDepartmentsById(db, usuario[0])

      usuarioALoguear = Usuario_Rutas(
         usuario[0],
         usuario[1],
         usuario[2],
         usuario[4],
         roles_usuario,
         permisos,
         paths_usuario,
         departamentos,
         )
         
      if not usuarioALoguear.activo:
         return {"error": "Usuario inactivo.", "status": 403}
         
      if not check_password_hash(usuario[3], password):
         return {"error": "Contraseña incorrecta.", "status": 401}
         
      if usuarioALoguear:
         login_user(usuarioALoguear)

      session['ultima_actividad'] = datetime.now().isoformat()
      session.permanent = True
         
      return {
         "mensaje": "Usuario logueado correctamente.",
         "usuario": {
            "idUsuario": usuarioALoguear.id,
            "username": usuarioALoguear.username,
            "nombre": usuarioALoguear.nombre,
            "activo": usuarioALoguear.activo,
            "rutas": usuarioALoguear.paths,
            }  
         }
   
   @staticmethod
   def getUsuario_login_service(db, idUsuario):

      if not idUsuario:
         return None

      usuario = UsuarioRepository.getUsuarioById(db, idUsuario)

      if not usuario:
         return None

      idUsuarioEncontrado = usuario["idUsuario"]

      paths = UsuarioRepository.getUserPaths(db, idUsuarioEncontrado)
      permisos = UsuarioRepository.getUserPermissionsById(db, idUsuarioEncontrado)
      roles = UsuarioRepository.getUserRolesById(db, idUsuarioEncontrado)
      departamentos = UsuarioRepository.getUserDepartmentsById(db, idUsuarioEncontrado)
      
      user = Usuario_Rutas(
         usuario["idUsuario"],
         usuario["username"],
         usuario["nombre"],
         usuario["activo"],
         roles,
         permisos,
         paths,
         departamentos
      )

      return user