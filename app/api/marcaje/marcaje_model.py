class Marcaje():
    def __init__(
            self,
            idMarcajeImportado,
            idEmpleado,
            nombre_empleado,
            departamento,
            area,
            dia,
            fecha,
            entrada_garita,
            entrada_area,
            salida_area,
            salida_garita,
            hora_simple,
            hora_doble,
            total_horas,
            horario_inicio,
            horario_fin,
            fecha_importacion,
        ):
        self.idMarcajeImportado = idMarcajeImportado
        self.idEmpleado = idEmpleado
        self.nombre_empleado = nombre_empleado
        self.departamento = departamento
        self.area = area
        self.dia = dia
        self.fecha = fecha
        self.entrada_garita = entrada_garita
        self.entrada_area = entrada_area
        self.salida_area = salida_area
        self.salida_garita = salida_garita
        self.hora_simple = hora_simple
        self.hora_doble = hora_doble
        self.total_horas = total_horas
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.fecha_importacion = fecha_importacion