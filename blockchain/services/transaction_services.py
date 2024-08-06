import datetime
import json as json_lib
from dateutil.parser import parse as parse_date


async def validate_transactions(event_data):
    return True
    transacciones = event_data["transacciones"]
    tipo_1 = None
    tipo_3 = None
    last_date = None

    for tx in transacciones:
        tipo = tx.get("tipo")
        detalle = tx.get("detalle")
        if not detalle:
            print("Transacción sin detalles:", tx)
            return False

        # Convertir fechas a objetos datetime para comparación
        if tipo == 1:
            fecha_inicio = detalle.get("fecha_inicio")
            if not fecha_inicio:
                print("Transacción tipo 1 sin fecha de inicio:", tx)
                return False
            fecha_inicio = parse_date(fecha_inicio)
            if tipo_1 is None:
                tipo_1 = detalle
            else:
                print("Más de una transacción tipo 1 encontrada")
                return False  # Más de una transacción tipo 1
            if last_date is not None and fecha_inicio <= last_date:
                print(
                    "Fecha de inicio de evento no es cronológica:",
                    fecha_inicio,
                    "<=",
                    last_date,
                )
                return False
            last_date = fecha_inicio
            print("Transacción tipo 1 válida:", tx)

        elif tipo == 2:
            fecha_ingreso = detalle.get("fecha_ingreso")
            usuario = detalle.get("usuario")
            validado = detalle.get("validado")
            if not fecha_ingreso or usuario is None or validado is None:
                print("Transacción tipo 2 con detalles faltantes:", tx)
                return False
            fecha_ingreso = parse_date(fecha_ingreso)
            print("Transacción tipo 2 válida:", tx)

        elif tipo == 3:
            fecha_cierre = detalle.get("fecha_cierre")
            if not fecha_cierre:
                print("Transacción tipo 3 sin fecha de cierre:", tx)
                return False
            fecha_cierre = parse_date(fecha_cierre)
            if tipo_3 is None:
                tipo_3 = detalle
            else:
                print("Más de una transacción tipo 3 encontrada")
                return False  # Más de una transacción tipo 3
            if last_date is not None and fecha_cierre <= last_date:
                print(
                    "Fecha de cierre de evento no es cronológica:",
                    fecha_cierre,
                    "<=",
                    last_date,
                )
                return False
            last_date = fecha_cierre
            print("Transacción tipo 3 válida:", tx)

        else:
            print("Transacción con tipo desconocido:", tx)
            return False

    if not tipo_1:
        print("No se encontró transacción tipo 1 (inicio de evento)")
        return False
    if not tipo_3:
        print("No se encontró transacción tipo 3 (cierre de evento)")
        return False

    print("Todas las transacciones son válidas")
    return True
