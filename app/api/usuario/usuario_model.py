from flask_login import UserMixin

class Usuario():
    def __init__(self, idUsuario, username, nombre, password_hash, activo, scope_departamentos_global, scope_permisos_global):
        self.idUsuario = idUsuario
        self.username = username
        self.nombre = nombre
        self.password_hash = password_hash
        self.activo = activo
        self.scope_departamentos_global = scope_departamentos_global
        self.scope_permisos_global = scope_permisos_global

class Usuario_Rutas(UserMixin):
    def __init__(self, idUsuario, username, nombre, activo, roles, permisos, paths, departamentos, scope_departamentos_global, scope_permisos_global, cambiar_password):
        self.id = idUsuario
        self.username = username
        self.nombre = nombre
        self.activo = activo
        self.roles = roles
        self.permisos = permisos
        self.paths = paths
        self.departamentos = departamentos
        self.scope_departamentos_global = scope_departamentos_global
        self.scope_permisos_global = scope_permisos_global
        self.cambiar_password = cambiar_password

    def tiene_permiso(self, permiso):
        if self.scope_permisos_global:
            return True

        return permiso in self.permisos
    
    def puede_ver_departamento(self, idDepartment):
        if self.scope_departamentos_global:
            return True
        
        return any(
            d["idDepartment"] == idDepartment
            for d in self.departamentos
        )
