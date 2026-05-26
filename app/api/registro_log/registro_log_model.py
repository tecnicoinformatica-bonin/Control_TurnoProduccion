class Registro():
    def __init__(self, idLog, idRegistro, idUsuario, fecha_modificacion, campo_modificado, valor_anterior, valor_nuevo):
        self.idLog = idLog
        self.idRegistro = idRegistro
        self.idUsuario = idUsuario
        self.fecha_modificacion = fecha_modificacion
        self.campo_modificado = campo_modificado
        self.valor_anterior = valor_anterior
        self.valor_nuevo = valor_nuevo
    