from datetime import datetime
from email.utils import format_datetime

def parse_fecha(fecha_str):
    if not fecha_str:
        return None

    formatos = [
        "%Y-%m-%dT%H:%M:%S",        # ISO
        "%Y-%m-%d %H:%M:%S",        # común
        "%Y-%m-%dT%H:%M",           # ISO sin segundos
        "%a, %d %b %Y %H:%M:%S GMT" # ya en formato RFC
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt)
        except ValueError:
            continue

    raise ValueError(f"Formato de fecha no soportado: {fecha_str}")