from flask import current_app

from datetime import timedelta, datetime, time, date

# FERIADOS_GT = {
#     "01-01", # Año nuevo
#     "05-01", # Día del Trabajador
#     "06-30", # Día del Ejército
#     "09-15", # Día de la Independencia
#     "10-20", # Día de la REvolución de 1944
#     "11-01", # Día de Todos los Santos
#     "12-25", # Navidad

#     # Villa Nueva
#     "12-08", # Feriado en Villa Nueva
# }

def es_feriado(fecha):
    return fecha.strftime("%m-%d") in current_app.config["FERIADOS_GT"]

def calcular_beneficios(fecha, hora_inicio, hora_fin):

    aplica_almuerzo = False
    aplica_cena = False
    cena_con_costo = False

    if not hora_inicio or not hora_fin:
        return {
            "aplica_almuerzo": False,
            "aplica_cena": False,
            "cena_con_costo": False,
        }

    fecha = obtener_fecha(fecha)
    hora_entrada = obtener_hora(hora_inicio)
    hora_salida = obtener_hora(hora_fin)

    # =====================================================
    # CENA SIN COSTO
    # =====================================================

    entrada_diurna = 5 <= hora_entrada <= 8

    salida_nocturna = (
        hora_salida >= 20
        or hora_salida <= 6
    )

    if entrada_diurna and salida_nocturna:
        aplica_cena = True

    # =====================================================
    # CENA CON COSTO
    # =====================================================

    if 13 <= hora_entrada <= 23.5:
        cena_con_costo = True

    # =====================================================
    # ALMUERZO
    # =====================================================

    es_sabado = fecha.weekday() == 5

    if (
        (es_sabado or es_feriado(fecha))
        and hora_salida >= 13
    ):
        aplica_almuerzo = True

    return {
        "aplica_almuerzo": aplica_almuerzo,
        "aplica_cena": aplica_cena,
        "cena_con_costo": cena_con_costo,
    }

def obtener_hora(hora):
    
    # Caso timedelta (MySQL TIME)
    if isinstance(hora, timedelta):
        return hora.seconds // 3600

    # Caso datetime.time
    if isinstance(hora, time):
        return hora.hour

    # Caso string "18:00" o "18:00:00"
    if isinstance(hora, str):
        return int(hora.split(":")[0])

    raise ValueError(f"Formato de hora no soportado: {type(hora)}")

def obtener_fecha(fecha):

    # Caso datetime.date
    if isinstance(fecha, date):
        return fecha

    # Caso string "2026-05-20"
    if isinstance(fecha, str):
        return datetime.strptime(fecha, "%Y-%m-%d").date()

    raise ValueError(f"Formato de fecha no soportado: {type(fecha)}")