

def compare_values_in_logs(registro_actual, datos_nuevos):
    logs = []

    for campo, valor_nuevo in datos_nuevos.items():

        valor_anterior = registro_actual[campo]

        if str(valor_anterior) != str(valor_nuevo):

            logs.append({
                "campo": campo,
                "anterior": valor_anterior,
                "nuevo": valor_nuevo
            })
    
    print(logs)

    return logs