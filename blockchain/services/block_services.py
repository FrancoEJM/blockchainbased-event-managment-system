import os
import glob
import time
from datetime import datetime
import json as json_lib
import sqlalchemy.orm as _orm
from dateutil.parser import parse as parse_date
from services import (
    blockchain_services as blc_sv,
    cryptography_services as crypto_sv,
    compression_services as compression_sv,
)
from models import blockchain_models as blc_md
import logging

PROTOCOL_VERSION = os.getenv("PROTOCOL_VERSION")

# def get_hash(block_number: int):
#     # Construir el nombre base del archivo del bloque
#     block_prefix = f"{block_number}_"

#     # Suponiendo que los archivos de bloques están en un directorio específico
#     block_directory = "/BLOCKCHAIN"

#     # Buscar el archivo que comienza con el número del bloque
#     previous_block_file = None
#     for filename in os.listdir(block_directory):
#         if filename.startswith(block_prefix):
#             previous_block_file = os.path.join(block_directory, filename)
#             break

#     if previous_block_file is None:
#         raise FileNotFoundError(
#             f"No se encontró el archivo del bloque anterior que comienza con: {block_prefix}"
#         )

#     with open(previous_block_file, "r") as file:
#         previous_block_data = json_lib.load(file)

#     # Obtener el hash del bloque anterior desde el JSON
#     previous_block_hash = previous_block_data.get("hash")

#     if previous_block_hash is None:
#         raise ValueError(
#             f"No se encontró el hash del bloque en el archivo: {previous_block_file}"
#         )

#     return previous_block_hash


# # Función para obtener el hash de un bloque
# def get_hash(block_number: int):
#     block_number_str = f"{block_number:08d}"
#     try:
#         # Buscar el archivo correspondiente al block_number en la carpeta BLOCKCHAIN
#         files = glob.glob(f"BLOCKCHAIN/{block_number_str}_*.txt")
#         if files:
#             with open(files[0], "r") as f:
#                 block_data = json_lib.load(f)

#                 # Verificar si la clave 'block_hash' existe en los datos
#                 if "block_hash" in block_data:
#                     return block_data["block_hash"]
#                 else:
#                     print(f"'block_hash' no encontrado en el archivo: {files[0]}")
#                     return "0" * 64
#         else:
#             print(
#                 f"No se encontró ningún archivo con el número de bloque {block_number_str}"
#             )
#             return "0" * 64
#     except Exception as e:
#         print(f"Error al obtener el hash del bloque anterior: {e}")
#         return None


# Función para obtener el hash de un bloque
# def get_hash(block_number: int):
#     block_number_str = f"{block_number:08d}"
#     try:
#         # Buscar el archivo correspondiente al block_number en la carpeta BLOCKCHAIN
#         zip_files = glob.glob(f"BLOCKCHAIN/{block_number_str}_*.zip")
#         if zip_files:
#             zip_filename = zip_files[0]
#             extract_to = "temp_extracted"
#             # Crear la carpeta temporal si no existe
#             if not os.path.exists(extract_to):
#                 os.makedirs(extract_to)
#             # Asegurarse de que la carpeta esté vacía antes de la extracción
#             for file in os.listdir(extract_to):
#                 os.remove(os.path.join(extract_to, file))
#             # Descomprimir el archivo .zip
#             compression_sv.unzip_file(zip_filename, extract_to)

#             # Buscar el archivo .txt descomprimido
#             txt_files = glob.glob(f"{extract_to}/{block_number_str}_*.txt")
#             if txt_files:
#                 with open(txt_files[0], "r") as f:
#                     block_data = json_lib.load(f)

#                     # Verificar si la clave 'block_hash' existe en los datos
#                     if "block_hash" in block_data:
#                         # Limpiar la carpeta temporal después de leer el archivo
#                         os.remove(txt_files[0])
#                         return block_data["block_hash"]
#                     else:
#                         print(
#                             f"'block_hash' no encontrado en el archivo: {txt_files[0]}"
#                         )
#                         return "0" * 64
#             else:
#                 print(
#                     f"No se encontró ningún archivo .txt en el archivo .zip: {zip_filename}"
#                 )
#                 return "0" * 64
#         else:
#             print(
#                 f"No se encontró ningún archivo .zip con el número de bloque {block_number_str}"
#             )
#             return "0" * 64
#     except Exception as e:
#         print(f"Error al obtener el hash del bloque: {e}")
#         return None


def get_hash(block_number: int):
    block_number_str = f"{block_number:08d}"
    try:
        # Buscar el archivo correspondiente al block_number en la carpeta BLOCKCHAIN
        zip_files = glob.glob(f"BLOCKCHAIN/{block_number_str}_*.zip")
        if zip_files:
            zip_filename = zip_files[0]
            extract_to = "temp_extracted"  # Crear la carpeta temporal si no existe
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)

            # Asegurarse de que la carpeta esté vacía antes de la extracción
            for file in os.listdir(extract_to):
                os.remove(os.path.join(extract_to, file))

            # Descomprimir el archivo .zip
            compression_sv.unzip_file(zip_filename, extract_to)

            # Buscar el archivo .txt descomprimido
            txt_files = glob.glob(f"{extract_to}/{block_number_str}_*.txt")
            if txt_files:
                # Asegurarse de cerrar el archivo después de leerlo
                with open(txt_files[0], "r") as f:
                    block_data = json_lib.load(f)

                # Verificar si la clave 'block_hash' existe en los datos
                if "block_hash" in block_data:
                    # Limpiar la carpeta temporal después de leer el archivo
                    os.remove(txt_files[0])
                    return block_data["block_hash"]
                else:
                    print(f"'block_hash' no encontrado en el archivo: {txt_files[0]}")
                    return "0" * 64
            else:
                print(
                    f"No se encontró ningún archivo .txt en el archivo .zip: {zip_filename}"
                )
                return "0" * 64
        else:
            print(
                f"No se encontró ningún archivo .zip con el número de bloque {block_number_str}"
            )
            return "0" * 64
    except Exception as e:
        print(f"Error al obtener el hash del bloque: {e}")
        return None


async def write_block(event_data: str, waited_time: float, db: _orm.Session):
    """
    Cabecera del bloque:
    1. Número de bloque ✅
    2. Timestamp ✅
    3. Hash del bloque anterior ✅
    4. Versión del protocolo #1.0.0 ✅
    Contenido del bloque:
    1. Id del evento ✅
    2. Nonce ✅
    3. Txs crypt ✅
    4. Hash del bloque ✅
    5. Firma digital del organizador del evento ✅
    6. Organización a la que pertenece ✅
    """
    # Datos de la cabecera del bloque
    block_number = await blc_sv.get_next_block_number(db)
    timestamp = time.time()
    previous_hash = get_hash(int(block_number) - 1)
    protocol_version = PROTOCOL_VERSION

    # Datos del cuerpo del bloque
    event_id = event_data["id_evento"]
    nonce = waited_time
    transactions = event_data["transacciones"]
    encrypted_transactions = crypto_sv.encrypt_transactions(transactions)
    # encrypted_transactions = transactions
    digital_signature = event_data["firma_digital"]
    organizer = event_data["organizador"]
    organization = event_data["organizacion"]

    # Ensamblar los datos del bloque
    block_data = {
        "block_number": f"{block_number:08d}",
        "timestamp": timestamp,
        "previous_hash": previous_hash,
        "protocol_version": protocol_version,
        "event_id": event_id,
        "nonce": nonce,
        "encrypted_transactions": encrypted_transactions,
        "organizer": organizer,
        "organization": organization,
        "digital_signature": digital_signature,
    }

    # Calcular el hash del bloque
    block_hash = await crypto_sv.calculate_block_hash(block_data)

    # Añadir el hash del bloque al block_data
    block_data["block_hash"] = block_hash

    # Verificar la existencia de la carpeta BLOCKCHAIN
    os.makedirs("BLOCKCHAIN", exist_ok=True)

    # Nombrar y escribir el archivo
    file_name = (
        f"BLOCKCHAIN/{block_number:08d}_{organization}_{event_id}_{int(timestamp)}.txt"
    )
    logging.info(f"Escribiendo el bloque: {file_name}")
    with open(file_name, "w") as block_file:
        block_file.write(json_lib.dumps(block_data, indent=4))

    return {
        "filename": file_name,
        "timestamp": timestamp,
        "block_number": int(block_number),
    }


async def record_block_data(
    event_data, filename, timestamp, block_number, db: _orm.Session
):
    event_id = event_data["id_evento"]
    organization = event_data["organizacion"]
    creator = event_data["organizador"]

    start_date = None
    end_date = None
    for transaction in event_data["transacciones"]:
        if transaction["tipo"] == 1:
            start_date = transaction["detalle"]["fecha_inicio"]
        elif transaction["tipo"] == 3:
            end_date = transaction["detalle"]["fecha_cierre"]

    # Convertir el timestamp float a una fecha
    if isinstance(timestamp, float):
        # Asumir que el float es una marca de tiempo en segundos desde el Epoch
        timestamp = datetime.fromtimestamp(timestamp).date()
    else:
        timestamp = parse_date(timestamp).date() if timestamp else None
    print(timestamp, type(timestamp))
    parsed_start_date = parse_date(start_date)
    parsed_end_date = parse_date(end_date)
    print("------------------------------------------------------------")
    # Crear un nuevo objeto BLOQUES
    new_block = blc_md.BLOQUES(
        id_bloque=block_number - 1,
        fecha_inicio=parsed_start_date,
        fecha_fin=parsed_end_date,
        id_evento=event_id,
        org=organization,
        creador=creator,
        path=filename,
        timestamp=timestamp,
        numero_bloque=block_number,
    )

    db.add(new_block)
    db.commit()
