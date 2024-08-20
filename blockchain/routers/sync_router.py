import os
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from services import (
    blockchain_services as blc_sv,
    util_services as util_sv,
    compression_services as compression_sv,
    database_services as db_sv,
)
from models import blockchain_models as blc_md
import aiohttp
import logging
import zipfile
import aiofiles
import sqlalchemy.orm as _orm
import sqlalchemy.ext.asyncio as _asyncio
import sqlalchemy.future as _future
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = _fastapi.APIRouter()


@router.post("/nodes/{node_id}/update_status")
async def update_status(
    node_id: int, status: bool, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    node = db.query(blc_md.NODOS).filter(blc_md.NODOS.id_nodo == node_id).first()
    if node:
        node.status = status
        db.commit()
        return {"message": "Node status updated successfully"}
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Node not found")


# @router.post("/blockchain/sync/current_data")
# async def sync_current_data(
#     ip: str = _fastapi.Query(...),
#     port: int = _fastapi.Query(...),
#     node_id: int = _fastapi.Query(...),
#     blocknumber: int = _fastapi.Query(...),
#     db: _orm.Session = _fastapi.Depends(db_sv.get_db),
# ):
#     # Contar el número de archivos en la carpeta BLOCKCHAIN
#     blockchain_path = "BLOCKCHAIN"
#     files = [f for f in os.listdir(blockchain_path) if f.endswith(".txt")]
#     files.sort()

#     # Enviar los archivos desde blocknumber en adelante
#     files_to_send = files[blocknumber:]
#     if not files_to_send:
#         return {"status": "success", "message": "No new files to sync"}

#     try:
#         # Enviar archivos
#         async with aiohttp.ClientSession() as session:
#             url = f"http://{ip}:{port}/blockchain/sync/files"
#             for filename in files_to_send:
#                 file_path = os.path.join(blockchain_path, filename)
#                 with open(file_path, "rb") as file:
#                     file_data = file.read()
#                     # Aquí deberás hacer una petición con el archivo leído
#                     async with session.post(url, data=file_data) as response:
#                         if response.status != 200:
#                             logging.error(
#                                 f"No se pudo enviar el archivo {filename} al nodo en {ip}:{port}"
#                             )
#     except Exception as e:
#         logging.error(f"Error al enviar archivos: {str(e)}")

#     return {"status": "success", "message": "Archivos enviados"}


@router.get("/blockchain/sync/current_data")
async def sync_current_data(blocknumber: int):
    # Define la carpeta donde se encuentran los bloques
    blockchain_dir = "BLOCKCHAIN"

    # Obtener todos los archivos de bloques en la carpeta
    all_files = os.listdir(blockchain_dir)

    # Filtrar los bloques que son posteriores al blocknumber recibido
    missing_blocks = [f for f in all_files if int(f.split("_")[0]) > blocknumber - 1]

    # Si no hay bloques faltantes, responder con un mensaje adecuado
    if not missing_blocks:
        return {
            "status": _fastapi.status.HTTP_100_CONTINUE,
            "message": "No missing blocks to sync.",
        }

    # Crear un archivo ZIP temporal para almacenar los bloques faltantes
    zip_filename = f"missing_blocks_{blocknumber}_to_{max([int(f.split('_')[0]) for f in missing_blocks])}.zip"
    zip_filepath = os.path.join(blockchain_dir, zip_filename)

    with zipfile.ZipFile(zip_filepath, "w") as zipf:
        for block in missing_blocks:
            block_path = os.path.join(blockchain_dir, block)
            zipf.write(block_path, os.path.basename(block_path))

    # Leer el archivo ZIP para enviarlo en la respuesta
    async def read_file(file_path):
        async with aiofiles.open(file_path, mode="rb") as f:
            return await f.read()

    file_data = await read_file(zip_filepath)

    # Borrar el archivo ZIP temporal después de leerlo
    os.remove(zip_filepath)

    # Retornar el archivo ZIP como respuesta
    return _fastapi.responses.StreamingResponse(
        io.BytesIO(file_data),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={zip_filename}"},
    )


# @router.get("/blockchain/sync/current_database_data")
# async def get_current_database_data(
#     block_number_from: int, db: _asyncio.AsyncSession = _fastapi.Depends(db_sv.get_db)
# ):
#     try:
#         # Consultar los registros en la base de datos local a partir del bloque especificado
#         result = db.execute(
#             _future.select(blc_md.BLOQUES)
#             .where(blc_md.BLOQUES.numero_bloque >= block_number_from)
#             .order_by(blc_md.BLOQUES.numero_bloque)
#         )
#         bloques = result.scalars().all()

#         # Transformar los registros en una lista de diccionarios
#         bloques_data = [
#             {
#                 "numero_bloque": bloque.numero_bloque,
#                 "fecha_inicio": bloque.fecha_inicio,
#                 "fecha_fin": bloque.fecha_fin,
#                 "id_evento": bloque.id_evento,
#                 "org": bloque.org,
#                 "creador": bloque.creador,
#                 "path": bloque.path,
#                 "timestamp": bloque.timestamp,
#             }
#             for bloque in bloques
#         ]

#         # Devolver los registros en formato JSON
#         return {"data": bloques_data}

#     except Exception as e:
#         logging.error(f"Error al obtener los datos de la base de datos: {e}")
#         raise _fastapi.HTTPException(
#             status_code=500, detail="Error al obtener los datos de la base de datos."
#         )


# @router.get("/blockchain/sync/current_database_data")
# async def current_database_data(
#     starting_block: int, db: AsyncSession = _fastapi.Depends(db_sv.get_db)
# ):
#     """
#     Endpoint para obtener datos de la base de datos desde un bloque inicial especificado.

#     - **starting_block**: Número del bloque desde el cual empezar a recuperar los datos.
#     """
#     try:
#         async with db.begin():
#             result = await db.execute(
#                 select(blc_md.BLOQUES).where(
#                     blc_md.BLOQUES.numero_bloque >= starting_block
#                 )
#             )
#             records = result.scalars().all()

#             # Convertir registros a formato JSON (o el formato necesario)
#             data = [
#                 record.to_dict() for record in records
#             ]  # Asumiendo que tienes un método to_dict() en tu modelo

#             return {"data": data}

#     except Exception as e:
#         logging.error(f"Error al obtener datos de la base de datos: {e}")
#         return {"error": "Error al obtener datos"}, 500


@router.get("/blockchain/sync/current_database_data")
async def sync_current_database_data(
    start_block: int = 0, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    try:
        # Realiza la consulta para obtener todos los registros con numero_bloque >= start_block
        query = select(blc_md.BLOQUES).where(
            blc_md.BLOQUES.numero_bloque >= start_block
        )
        result = db.execute(query)
        blocks = result.fetchall()
        logging.info("hago la query")
        # Convertir los resultados a una lista de diccionarios
        blocks_list = [dict(zip(result.keys(), row)) for row in blocks]

        return {"status": _fastapi.status.HTTP_200_OK, "data": blocks_list}

    except Exception as e:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
