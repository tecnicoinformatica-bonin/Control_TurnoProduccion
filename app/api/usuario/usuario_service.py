from datetime import datetime

from flask import redirect, session, url_for
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
               "scope_departamentos_global": row[5],               
               "scope_permisos_global": row[6],               
            }
            usuarios.append(usuario)

         return usuarios
      except Exception as ex:
         return {"error": f"No se puede listar los usuarios. {ex}"}
      
   @staticmethod
   def getUsuarioById_service(db, idUsuario):
      try:
         data = UsuarioRepository.getUsuarioById(db, idUsuario)
         usuario =  {
            "idUsuario": data["idUsuario"],
            "username": data["username"],
            "nombre": data["nombre"],
            "activo": data["activo"],
            "scope_departamentos_global": data["scope_departamentos_global"],
            "scope_permisos_global": data["scope_permisos_global"],
         }

         return usuario
      except Exception as ex:
         raise Exception(f"No se puede listar los usuarios. {str(ex)}")
      
   @staticmethod
   def createUsuario_service(db, data):
      try:
         username = data.get("username")
         nombre = data.get("nombre")
         password = data.get("password")
         activo = bool(data.get("activo"))
         scope_departamentos_global = bool(data.get("scope_departamentos_global"))
         scope_permisos_global = bool(data.get("scope_permisos_global"))
         
         if not username or not password:
            return {"error": "Nombre de usuario y contraseña son obligatorios"}, 400
         
         return UsuarioRepository.createUsuario(db, username, nombre, password, activo, scope_departamentos_global, scope_permisos_global)
         
      except Exception as ex:
         raise Exception(f"No se pudo crear el usuario. {str(ex)}")

   @staticmethod
   def updateUsuario_service(db, data):
      try:
         idUsuario = data.get("idUsuario")
         nombre = data.get("nombre")
         activo = bool(data.get("activo"))
         scope_departamentos_global = bool(data.get("scope_departamentos_global"))
         scope_permisos_global = bool(data.get("scope_permisos_global"))
         
         required_fields = {
                  "idUsuario": idUsuario, 
                  "nombre": nombre,
                  "activo": activo,
                  "scope_departamentos_global": scope_departamentos_global,
                  "scope_permisos_global": scope_permisos_global,
               }
         
         missing_fields = [key for key, value in required_fields.items() if value is None or value == ""]

         if missing_fields:
               return {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"}
         
         return UsuarioRepository.updateUsuario(db, idUsuario, nombre, activo, scope_departamentos_global, scope_permisos_global)
      
      except Exception as ex:
         raise Exception(f"No se pudo actualizar el usuario. {str(ex)}")
      
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
      
      idUsuarioEncontrado = usuario["idUsuario"]
         
      paths_usuario = UsuarioRepository.getUserPaths(db, idUsuarioEncontrado)
      permisos = UsuarioRepository.getUserPermissionsById(db, idUsuarioEncontrado)
      roles_usuario = UsuarioRepository.getUserRolesById(db, idUsuarioEncontrado)
      departamentos = UsuarioRepository.getUserDepartmentsById(db, idUsuarioEncontrado)

      usuarioALoguear = Usuario_Rutas(
         usuario["idUsuario"],
         usuario["username"],
         usuario["nombre"],
         usuario["activo"],
         roles_usuario,
         permisos,
         paths_usuario,
         departamentos,
         usuario["scope_departamentos_global"],
         usuario["scope_permisos_global"],
         )
         
      if not usuarioALoguear.activo:
         return {"error": "Usuario inactivo.", "status": 403}
         
      if not check_password_hash(usuario["password_hash"], password):
         return {"error": "Contraseña incorrecta.", "status": 401}
      
      # if usuario["cambiar_password"] == 1:
      #    return redirect(url_for(
      #       "usuario_template.change_password",
      #       username = usuario["username"]
      #    ))
         
      if usuarioALoguear:
         login_user(usuarioALoguear)

      session['ultima_actividad'] = datetime.now().isoformat()
      session.permanent = True
         
      return {
            "idUsuario": usuarioALoguear.id,
            "username": usuarioALoguear.username,
            "nombre": usuarioALoguear.nombre,
            "activo": usuarioALoguear.activo,
            "rutas": usuarioALoguear.paths,
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
         departamentos,
         usuario["scope_departamentos_global"],
         usuario["scope_permisos_global"],
      )

      return user