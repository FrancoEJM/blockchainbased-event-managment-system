from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json as json_lib
import fastapi as _fastapi
import datetime
from dateutil.parser import parse as parse_date

router = _fastapi.APIRouter()


@router.post("/TEST-verify")
async def verify_event_data(event_data: str):
    try:
        # Convertir la cadena de texto JSON a un objeto JSON
        event_data_json = json_lib.loads(event_data)

        # Extraer la información necesaria del objeto JSON
        transacciones = event_data_json["transacciones"]
        llave_publica = event_data_json["llave_publica"]
        firma_digital = event_data_json["firma_digital"]

        # Convertir transacciones a JSON y luego a bytes
        transactions_json = json_lib.dumps(transacciones, separators=(",", ":")).encode(
            "utf-8"
        )

        print(f"Transacciones JSON (bytes):\n{transactions_json}")

        # Cargar la clave pública desde el PEM
        public_key_pem = llave_publica.encode()
        print(f"Public Key PEM:\n{public_key_pem.decode()}")

        public_key = serialization.load_pem_public_key(public_key_pem)

        # Convertir la firma digital de hex a bytes
        firma_digital_bytes = bytes.fromhex(firma_digital)
        print(f"Firma Digital (hex):\n{firma_digital}")
        print(f"Firma Digital (bytes):\n{firma_digital_bytes}")

        # Verificar la firma
        public_key.verify(
            firma_digital_bytes,
            transactions_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        print("La firma digital es válida")
        return {"status": "success", "message": "La firma digital es válida"}

    except Exception as e:
        print(f"Error verificando la firma digital: {str(e)}")
        raise HTTPException(
            status_code=400, detail=f"La firma digital no es válida: {str(e)}"
        )


# @router.post("/test-TXs")
# async def validate_transactions(event_data: str):
#     event_data_json = json_lib.loads(event_data)
#     transacciones = event_data_json["transacciones"]
#     tipo_1 = None
#     tipo_3 = None
#     last_date = None

#     for tx in transacciones:
#         tipo = tx.get("tipo")
#         detalle = tx.get("detalle")
#         if not detalle:
#             print("Transacción sin detalles:", tx)
#             return False

#         # Convertir fechas a objetos datetime para comparación
#         if tipo == 1:
#             fecha_inicio = detalle.get("fecha_inicio")
#             if not fecha_inicio:
#                 print("Transacción tipo 1 sin fecha de inicio:", tx)
#                 return False
#             fecha_inicio = parse_date(fecha_inicio)
#             if tipo_1 is None:
#                 tipo_1 = detalle
#             else:
#                 print("Más de una transacción tipo 1 encontrada")
#                 return False  # Más de una transacción tipo 1
#             if last_date is not None and fecha_inicio <= last_date:
#                 print(
#                     "Fecha de inicio de evento no es cronológica:",
#                     fecha_inicio,
#                     "<=",
#                     last_date,
#                 )
#                 return False
#             last_date = fecha_inicio
#             print("Transacción tipo 1 válida:", tx)

#         elif tipo == 2:
#             fecha_ingreso = detalle.get("fecha_ingreso")
#             usuario = detalle.get("usuario")
#             validado = detalle.get("validado")
#             if not fecha_ingreso or usuario is None or validado is None:
#                 print("Transacción tipo 2 con detalles faltantes:", tx)
#                 return False
#             fecha_ingreso = parse_date(fecha_ingreso)
#             print("Transacción tipo 2 válida:", tx)

#         elif tipo == 3:
#             fecha_cierre = detalle.get("fecha_cierre")
#             if not fecha_cierre:
#                 print("Transacción tipo 3 sin fecha de cierre:", tx)
#                 return False
#             fecha_cierre = parse_date(fecha_cierre)
#             if tipo_3 is None:
#                 tipo_3 = detalle
#             else:
#                 print("Más de una transacción tipo 3 encontrada")
#                 return False  # Más de una transacción tipo 3
#             if last_date is not None and fecha_cierre <= last_date:
#                 print(
#                     "Fecha de cierre de evento no es cronológica:",
#                     fecha_cierre,
#                     "<=",
#                     last_date,
#                 )
#                 return False
#             last_date = fecha_cierre
#             print("Transacción tipo 3 válida:", tx)

#         else:
#             print("Transacción con tipo desconocido:", tx)
#             return False

#     if not tipo_1:
#         print("No se encontró transacción tipo 1 (inicio de evento)")
#         return False
#     if not tipo_3:
#         print("No se encontró transacción tipo 3 (cierre de evento)")
#         return False

#     print("Todas las transacciones son válidas")
#     return True


@router.post("/test-TXs")
async def validate_transactions(request: _fastapi.Request):
    event_data = await request.json()
    # event_data_json = json_lib.loads(event_data)
    transacciones = event_data["transacciones"]
    tipo_1 = None
    tipo_3 = None
    fecha_inicio = None
    fecha_cierre = None

    # Primero validamos las transacciones tipo 1 y tipo 3
    for tx in transacciones:
        tipo = tx.get("tipo")
        detalle = tx.get("detalle")
        if not detalle:
            print("Transacción sin detalles:", tx)
            return {"status": "error", "message": "Transacción sin detalles"}

        if tipo == 1:
            fecha_inicio = detalle.get("fecha_inicio")
            if not fecha_inicio:
                print("Transacción tipo 1 sin fecha de inicio:", tx)
                return {
                    "status": "error",
                    "message": "Transacción tipo 1 sin fecha de inicio",
                }
            fecha_inicio = parse_date(fecha_inicio)
            if tipo_1 is None:
                tipo_1 = detalle
            else:
                print("Más de una transacción tipo 1 encontrada")
                return {
                    "status": "error",
                    "message": "Más de una transacción tipo 1 encontrada",
                }
            print("Transacción tipo 1 válida:", tx)

        elif tipo == 3:
            fecha_cierre = detalle.get("fecha_cierre")
            if not fecha_cierre:
                print("Transacción tipo 3 sin fecha de cierre:", tx)
                return {
                    "status": "error",
                    "message": "Transacción tipo 3 sin fecha de cierre",
                }
            fecha_cierre = parse_date(fecha_cierre)
            if tipo_3 is None:
                tipo_3 = detalle
            else:
                print("Más de una transacción tipo 3 encontrada")
                return {
                    "status": "error",
                    "message": "Más de una transacción tipo 3 encontrada",
                }
            print("Transacción tipo 3 válida:", tx)

    # Verificar que las transacciones tipo 1 y tipo 3 existan
    if not tipo_1:
        print("No se encontró transacción tipo 1 (inicio de evento)")
        return {
            "status": "error",
            "message": "No se encontró transacción tipo 1 (inicio de evento)",
        }
    if not tipo_3:
        print("No se encontró transacción tipo 3 (cierre de evento)")
        return {
            "status": "error",
            "message": "No se encontró transacción tipo 3 (cierre de evento)",
        }

    # Validar las transacciones tipo 2
    for tx in transacciones:
        tipo = tx.get("tipo")
        detalle = tx.get("detalle")

        if tipo == 2:
            fecha_ingreso = detalle.get("fecha_ingreso")
            usuario = detalle.get("usuario")
            validado = detalle.get("validado")
            if not fecha_ingreso or usuario is None or validado is None:
                print("Transacción tipo 2 con detalles faltantes:", tx)
                return {
                    "status": "error",
                    "message": "Transacción tipo 2 con detalles faltantes",
                }
            fecha_ingreso = parse_date(fecha_ingreso)
            if fecha_inicio is not None and fecha_ingreso < fecha_inicio:
                print(
                    "Fecha de ingreso es anterior a la fecha de inicio del evento:",
                    fecha_ingreso,
                    "<",
                    fecha_inicio,
                )
                return {
                    "status": "error",
                    "message": "Fecha de ingreso es anterior a la fecha de inicio del evento",
                }
            if fecha_cierre is not None and fecha_ingreso > fecha_cierre:
                print(
                    "Fecha de ingreso es posterior a la fecha de cierre del evento:",
                    fecha_ingreso,
                    ">",
                    fecha_cierre,
                )
                return {
                    "status": "error",
                    "message": "Fecha de ingreso es posterior a la fecha de cierre del evento",
                }
            print("Transacción tipo 2 válida:", tx)

    print("Todas las transacciones son válidas")
    return {"status": "success", "message": "Todas las transacciones son válidas"}
