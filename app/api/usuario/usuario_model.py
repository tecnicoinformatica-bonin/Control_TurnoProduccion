from flask_login import UserMixin

class Usuario():
    def __init__(self, idUsuario, username, nombre, password_hash, activo):
        self.idUsuario = idUsuario
        self.username = username
        self.nombre = nombre
        self.password_hash = password_hash
        self.activo = activo

class Usuario_Rutas(UserMixin):
    def __init__(self, idUsuario, username, nombre, activo, roles, permisos, paths):
        self.id = idUsuario
        self.username = username
        self.nombre = nombre
        self.activo = activo
        self.roles = roles
        self.permisos = permisos
        self.paths = paths