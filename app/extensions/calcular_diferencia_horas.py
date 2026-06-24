from datetime import datetime, timedelta
import math

def to_timedelta(hora):
    if hora is None:
        return None

    if isinstance(hora, timedelta):
        return hora

    if isinstance(hora, str):
        h, m, s = map(int, hora.split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)

    raise ValueError(f"Formato no soportado: {type(hora)}")


def floor_half(hours):
    return math.floor(hours * 2) / 2


def calcular_diferencia_horas(
    fecha,
    hora_inicio_empleado,
    hora_fin_empleado,
    hora_inicio_digitada,
    hora_fin_digitada
):
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

    inicio_emp = to_timedelta(hora_inicio_empleado)
    fin_emp = to_timedelta(hora_fin_empleado)

    inicio_sup = to_timedelta(hora_inicio_digitada)
    fin_sup = to_timedelta(hora_fin_digitada)

    if None in (inicio_emp, fin_emp, inicio_sup, fin_sup):
        return 0
    
     # Sábado o domingo
    if fecha.weekday() in (5, 6):
        if fin_sup < inicio_sup:
            fin_sup += timedelta(days=1)

        total_horas = (fin_sup - inicio_sup).total_seconds() / 3600

        return floor_half(total_horas)

    if fecha.weekday() == 4:
        fin_emp = to_timedelta("15:00:00")

    entrada_extra = 0
    salida_extra = 0

    if inicio_sup < inicio_emp:
        entrada_extra = (inicio_emp - inicio_sup).total_seconds() / 3600

    if fin_sup > fin_emp:
        salida_extra = (fin_sup - fin_emp).total_seconds() / 3600

    total = entrada_extra + salida_extra

    return floor_half(total)