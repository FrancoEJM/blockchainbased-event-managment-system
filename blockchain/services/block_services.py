import os
import glob
import time
from datetime import datetime
import json as json_lib
import sqlalchemy.orm as _orm
from dateutil.parser import parse as parse_date
from services import blockchain_services as blc_sv, cryptography_services as crypto_sv
from models import blockchain_models as blc_md

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


# Función para obtener el hash de un bloque
def get_hash(block_number: int):
    block_number = f"{block_number:08d}"
    try:
        # Buscar el archivo correspondiente al block_number en la carpeta BLOCKCHAIN
        files = glob.glob(f"BLOCKCHAIN/{block_number}_*.txt")
        if files:
            with open(files[0], "r") as f:
                block_data = json_lib.load(f)
                return block_data["block_hash"]
        return "0" * 64
    except Exception as e:
        print(f"Error al obtener el hash del bloque anterior: {e}")
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

    block_number = await blc_sv.get_next_block_number(db)

    timestamp = time.time()

    previous_hash = get_hash(int(block_number) - 1)

    protocol_version = PROTOCOL_VERSION

    event_id = event_data["id_evento"]

    nonce = waited_time

    transactions = event_data["transacciones"]
    encrypted_transactions = crypto_sv.encrypt_transactions(transactions)

    digital_signature = event_data["firma_digital"]

    organizer = event_data["organizador"]

    organization = event_data["organizacion"]

    # Ensamblar los datos del bloque
    block_data = {
        "block_number": block_number,
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
        f"BLOCKCHAIN/{block_number}_{organization}_{event_id}_{int(timestamp)}.txt"
    )
    with open(file_name, "w") as block_file:
        block_file.write(json_lib.dumps(block_data, indent=4))

    return {"filename": file_name, "timestamp": timestamp}


async def record_block_data(event_data, filename, timestamp, db: _orm.Session):
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
        fecha_inicio=parsed_start_date,
        fecha_fin=parsed_end_date,
        id_evento=event_id,
        org=organization,
        creador=creator,
        path=filename,
        timestamp=timestamp,
    )

    db.add(new_block)
    db.commit()
