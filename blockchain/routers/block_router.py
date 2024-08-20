import fastapi as _fastapi
from services import (
    blockchain_services as blc_sv,
    database_services as db_sv,
    block_services as block_sv,
    node_services as node_sv,
    compression_services as compression_sv,
)
import sqlalchemy.orm as _orm
import os
import shutil
import json
import datetime
from models import blockchain_models as blc_md
import random
from datetime import datetime
import logging

router = _fastapi.APIRouter()
BLOCKCHAIN_DIR = os.path.join(os.getcwd(), "BLOCKCHAIN")
TEMP_EXTRACTED_DIR = os.path.join(os.getcwd(), "temp_extracted")


@router.post("/blockchain/block")
async def add_new_block(
    request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    data = await request.json()
    event_data = data.get("event_data")
    waited_time = data.get("waited_time")
    response = await blc_sv.add_new_block(event_data, waited_time, db)
    if response["status"] != 200:
        return {"status": response["status"], "message": response["message"]}

    # await block_sv.record_block_data(
    #     event_data,
    #     response["file_name"],
    #     response["timestamp"],
    #     response["block_number"],
    #     db,
    # )
    # await node_sv.record_node_data(response["node_id"], waited_time, db)

    return {"status": response["status"], "message": response["message"]}


# @router.post("/blockchain/block/latest")
# async def receive_block(
#     file: _fastapi.UploadFile = _fastapi.File(...),
#     db: _orm.Session = _fastapi.Depends(db_sv.get_db),
# ):
#     logging.info(f"El archivo recibido es {file.filename}")

#     # Construir la ruta completa del archivo ZIP
#     zip_file_location = os.path.join(BLOCKCHAIN_DIR, file.filename)
#     logging.info(f"Ruta del archivo ZIP antes de normalizar: {zip_file_location}")

#     # Normalizar la ruta para asegurar separadores consistentes
#     zip_file_location = os.path.normpath(zip_file_location)
#     logging.info(f"Ruta del archivo ZIP después de normalizar: {zip_file_location}")

#     # Convertir la ruta a un formato relativo con separadores '/'
#     zip_file_location = os.path.relpath(zip_file_location, start=BLOCKCHAIN_DIR)
#     zip_file_location = zip_file_location.replace(os.sep, "/")
#     logging.info(
#         f"Ruta del archivo ZIP después de convertir a relativa y normalizar: {zip_file_location}"
#     )

#     # Verificar si el directorio BLOCKCHAIN existe, si no, crearlo
#     if not os.path.exists(BLOCKCHAIN_DIR):
#         os.makedirs(BLOCKCHAIN_DIR)
#         logging.info(f"Directorio {BLOCKCHAIN_DIR} creado")

#     try:
#         # Guardar el archivo ZIP recibido en /BLOCKCHAIN/
#         with open(zip_file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         logging.info(f"Archivo ZIP guardado correctamente en {zip_file_location}")

#         # Verificar si el archivo ZIP se ha guardado
#         if not os.path.isfile(zip_file_location):
#             raise _fastapi.HTTPException(
#                 status_code=500,
#                 detail=f"Archivo ZIP no encontrado: {zip_file_location}",
#             )

#         # Crear el directorio temporal para descomprimir
#         if not os.path.exists(TEMP_EXTRACTED_DIR):
#             os.makedirs(TEMP_EXTRACTED_DIR)
#             logging.info(f"Directorio temporal {TEMP_EXTRACTED_DIR} creado")

#         # Descomprimir el archivo ZIP
#         compression_sv.unzip_file(zip_file_location, TEMP_EXTRACTED_DIR)
#         logging.info(f"Archivo ZIP descomprimido en {TEMP_EXTRACTED_DIR}")

#         # Encontrar el archivo .txt dentro del directorio extraído
#         txt_files = [f for f in os.listdir(TEMP_EXTRACTED_DIR) if f.endswith(".txt")]
#         if not txt_files:
#             raise _fastapi.HTTPException(
#                 status_code=500, detail="No se encontró ningún archivo .txt en el ZIP"
#             )

#         # Leer y procesar el archivo .txt del bloque
#         txt_file_path = os.path.join(TEMP_EXTRACTED_DIR, txt_files[0])
#         logging.info(f"Ruta del archivo .txt: {txt_file_path}")

#         with open(txt_file_path, "r", encoding="utf-8") as f:
#             block_data = json.load(f)

#         # Extraer datos del bloque
#         block_number = block_data.get("block_number")
#         timestamp = datetime.fromtimestamp(block_data.get("timestamp")).strftime(
#             "%Y-%m-%d"
#         )
#         event_id = block_data.get("event_id")
#         organization = block_data.get("organization")
#         creator = block_data.get("organizer")

#         # Crear un nuevo registro de bloque
#         new_block = blc_md.BLOQUES(
#             id_bloque=int(block_number) + 1,
#             path="BLOCKCHAIN/" + zip_file_location,
#             id_evento=event_id,
#             org=organization,
#             fecha_inicio=None,
#             fecha_fin=None,
#             creador=creator,
#             timestamp=timestamp,
#             numero_bloque=int(block_number),
#         )
#         db.add(new_block)
#         db.commit()

#         return {
#             "status": "success",
#             "status_code": 200,
#             "message": "Block received and processed successfully",
#         }
#     except Exception as e:
#         logging.error(f"Error receiving block: {str(e)}")
#         db.rollback()
#         raise _fastapi.HTTPException(
#             status_code=500, detail=f"Error receiving block: {str(e)}"
#         )
#     finally:
#         # Limpiar archivos temporales
#         for txt_file in os.listdir(TEMP_EXTRACTED_DIR):
#             logging.info(
#                 f"Elimino archivo temporal {os.path.join(TEMP_EXTRACTED_DIR, txt_file)}"
#             )
#             os.remove(os.path.join(TEMP_EXTRACTED_DIR, txt_file))
#         os.rmdir(TEMP_EXTRACTED_DIR)


@router.post("/blockchain/block/latest")
async def receive_block(
    file: _fastapi.UploadFile = _fastapi.File(...),
    db: _orm.Session = _fastapi.Depends(db_sv.get_db),
):
    logging.info(f"El archivo recibido es {file.filename}")

    # Construir la ruta completa del archivo ZIP
    zip_file_location = os.path.join(BLOCKCHAIN_DIR, file.filename)
    logging.info(f"Ruta del archivo ZIP antes de normalizar: {zip_file_location}")

    # Normalizar la ruta para asegurar separadores consistentes
    zip_file_location = os.path.normpath(zip_file_location)
    logging.info(f"Ruta del archivo ZIP después de normalizar: {zip_file_location}")

    # Convertir la ruta a un formato relativo con separadores '/'

    # Obtener la ruta relativa a partir del directorio de trabajo actual
    zip_file_location = os.path.relpath(zip_file_location, start=os.getcwd())

    # Reemplazar los separadores de ruta con '/'
    zip_file_location = zip_file_location.replace(os.sep, "/")

    logging.info(
        f"Ruta del archivo ZIP después de convertir a relativa y normalizar: {zip_file_location}"
    )

    # Verificar si el directorio BLOCKCHAIN existe, si no, crearlo
    if not os.path.exists(BLOCKCHAIN_DIR):
        os.makedirs(BLOCKCHAIN_DIR)
        logging.info(f"Directorio {BLOCKCHAIN_DIR} creado")

    try:
        # Guardar el archivo ZIP recibido en /BLOCKCHAIN/
        with open(zip_file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logging.info(f"Archivo ZIP guardado correctamente en {zip_file_location}")

        # Verificar si el archivo ZIP se ha guardado
        if not os.path.isfile(zip_file_location):
            raise _fastapi.HTTPException(
                status_code=500,
                detail=f"Archivo ZIP no encontrado: {zip_file_location}",
            )

        # Crear el directorio temporal para descomprimir
        if not os.path.exists(TEMP_EXTRACTED_DIR):
            os.makedirs(TEMP_EXTRACTED_DIR)
            logging.info(f"Directorio temporal {TEMP_EXTRACTED_DIR} creado")

        # Descomprimir el archivo ZIP
        compression_sv.unzip_file(zip_file_location, TEMP_EXTRACTED_DIR)
        logging.info(f"Archivo ZIP descomprimido en {TEMP_EXTRACTED_DIR}")

        # Encontrar el archivo .txt dentro del directorio extraído
        txt_files = [f for f in os.listdir(TEMP_EXTRACTED_DIR) if f.endswith(".txt")]
        if not txt_files:
            raise _fastapi.HTTPException(
                status_code=500, detail="No se encontró ningún archivo .txt en el ZIP"
            )

        # Leer y procesar el archivo .txt del bloque
        txt_file_path = os.path.join(TEMP_EXTRACTED_DIR, txt_files[0])
        logging.info(f"Ruta del archivo .txt: {txt_file_path}")

        with open(txt_file_path, "r", encoding="utf-8") as f:
            block_data = json.load(f)

        # Extraer datos del bloque
        block_number = block_data.get("block_number")
        timestamp = datetime.fromtimestamp(block_data.get("timestamp")).strftime(
            "%Y-%m-%d"
        )
        event_id = block_data.get("event_id")
        organization = block_data.get("organization")
        creator = block_data.get("organizer")

        # Crear un nuevo registro de bloque
        new_block = blc_md.BLOQUES(
            id_bloque=int(block_number) + 1,
            path="BLOCKCHAIN/" + zip_file_location,
            id_evento=event_id,
            org=organization,
            fecha_inicio=None,
            fecha_fin=None,
            creador=creator,
            timestamp=timestamp,
            numero_bloque=int(block_number),
        )
        db.add(new_block)
        db.commit()

        return {
            "status": "success",
            "status_code": 200,
            "message": "Block received and processed successfully",
        }
    except Exception as e:
        logging.error(f"Error receiving block: {str(e)}")
        db.rollback()
        raise _fastapi.HTTPException(
            status_code=500, detail=f"Error receiving block: {str(e)}"
        )
    finally:
        # Limpiar archivos temporales
        for txt_file in os.listdir(TEMP_EXTRACTED_DIR):
            logging.info(
                f"Elimino archivo temporal {os.path.join(TEMP_EXTRACTED_DIR, txt_file)}"
            )
            os.remove(os.path.join(TEMP_EXTRACTED_DIR, txt_file))
        os.rmdir(TEMP_EXTRACTED_DIR)
