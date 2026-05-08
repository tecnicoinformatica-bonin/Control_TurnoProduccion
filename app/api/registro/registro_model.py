class Registro():
    def __init__(self, idRegistro, idProgramacion, idEmpleado, hora_inicio, hora_fin, idLinea, idProceso, aplica_almuerzo, aplica_cena, aplica_transporte, observacion_transporte, fecha, idCentro, badgeNumber):
        self.idRegistro = idRegistro
        self.idProgramacion = idProgramacion
        self.idEmpleado = idEmpleado
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.idLinea = idLinea
        self.idProceso = idProceso
        self.aplica_almuerzo = aplica_almuerzo
        self.aplica_cena = aplica_cena
        self.aplica_transporte = aplica_transporte
        self.observacion_transporte = observacion_transporte
        self.fecha = fecha
        self.idCentro = idCentro
        self.badgeNumber = badgeNumber