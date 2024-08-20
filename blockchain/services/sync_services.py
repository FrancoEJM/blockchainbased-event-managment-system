from services import (
    blockchain_services as blc_sv,
    util_services as util_sv,
    compression_services as compression_sv,
    database_services as db_sv,
)
import sqlalchemy.orm as _orm
import sqlalchemy.future as _future
import sqlalchemy as _sqlalchemy
import aiohttp
import asyncio
import logging
import os
import zipfile
import fastapi as _fastapi
from models import blockchain_models as blc_md
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import httpx

BLOCKCHAIN_DIR = "/BLOCKCHAIN"
IP = os.getenv("IP")  # Por ejemplo, 'localhost'
PORT = os.getenv("PORT")  # Por ejemplo, '8001'


async def notify_status_change(id: int, status: bool, db: _orm.Session):
    active_nodes = await blc_sv.get_active_nodes(db)
    nodes_to_notify = [node for node in active_nodes if node.id_nodo != id]
    nodes_to_notify_number = len(nodes_to_notify)
    logging.info(f"Nodos activos: {nodes_to_notify_number}")
    if nodes_to_notify_number:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for node in nodes_to_notify:
                url = f"http://{node.ip}:{node.port}/nodes/{id}/update_status"
                task = send_status_update(
                    session, url, status, node.id_nodo, node.ip, node.port
                )
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            return responses
    else:
        return []


async def send_status_update(
    session: aiohttp.ClientSession,
    url: str,
    status: bool,
    node_id: int,
    ip: str,
    port: int,
):
    try:
        async with session.post(
            url, params={"status": str(status).lower()}
        ) as response:
            # Recoger el código de estado y otros detalles relevantes
            return {
                "status_code": response.status,
                "node_id": node_id,
                "ip": ip,
                "port": port,
                "url": url,
            }
    except Exception as e:
        # En caso de error, manejar la excepción y registrar el error
        return {
            "status_code": 500,
            "node_id": node_id,
            "ip": ip,
            "port": port,
            "url": url,
            "error": str(e),
        }


async def update_and_notify_status(
    ip: str, port: int, status: bool, node_id: int, db: _orm.Session
):
    try:
        # Actualiza el estado del nodo en la base de datos
        await blc_sv.update_node_status(ip, port, status, db)
        logging.info("Estado actualizado correctamente en la base de datos")

        # Notifica el cambio de estado a otros nodos
        logging.info("Compartiendo información con los nodos de la red...")
        responses = await notify_status_change(node_id, status, db)

        for response in responses:
            if response["status_code"] == 200:
                logging.info(
                    f"Estado compartido exitosamente con el nodo {response['node_id']} ({response['ip']}:{response['port']})"
                )
            else:
                logging.error(
                    f"Error al compartir estado con el nodo {response['node_id']} ({response['ip']}:{response['port']}), código de estado {response['status_code']}"
                )
    except Exception as e:
        logging.error(f"Ocurrió un error: {e}")
    finally:
        db.close()


# async def spread_block(filename: str, db: _orm.Session):
#     async def send_block_to_node(node_ip: str, block_data: bytes):
#         url = f"http://{node_ip}/blockchain/block/latest"
#         async with aiohttp.ClientSession() as session:
#             try:
#                 async with session.post(url, data=block_data) as response:
#                     if response.status == 200:
#                         print(f"Block successfully sent to node {node_ip}")
#                     else:
#                         print(
#                             f"Failed to send block to node {node_ip}. Status code: {response.status}"
#                         )
#             except Exception as e:
#                 print(f"Error sending block to node {node_ip}: {e}")

#     # Leer el contenido del archivo
#     # file_path = os.path.join(BLOCKCHAIN_DIR, filename)
#     logging.info(f"Enviando el archivo {filename}")
#     with open(filename, "rb") as file:
#         block_data = file.read()

#     # Obtener nodos activos
#     active_nodes = await blc_sv.get_active_nodes(db)
#     formatted_nodes = util_sv.convert_nodes(active_nodes)
#     logging.info(f"formated_nodes:{formatted_nodes}")
#     nodes = [{"ip": node["ip"]} for node in formatted_nodes]
#     logging.info(f"Todos los nodos activos:{nodes}")
#     # Enviar el bloque a todos los nodos
#     tasks = [send_block_to_node(node["ip"], block_data) for node in nodes]
#     await asyncio.gather(*tasks)


async def spread_block(filename: str, db: _orm.Session):
    async def send_block_to_node(node_ip: str, block_data: bytes, filename: str):
        url = f"http://{node_ip}/blockchain/block/latest"
        async with aiohttp.ClientSession() as session:
            try:
                form_data = aiohttp.FormData()
                form_data.add_field(
                    "file",  # Este nombre debe coincidir con el parámetro `file` del endpoint
                    block_data,
                    filename=filename,
                    content_type="application/octet-stream",
                )

                async with session.post(url, data=form_data) as response:
                    logging.info(f"Respuesta de block/latest {response.status}")
                    if response.status == 200:
                        print(f"Block successfully sent to node {node_ip}")
                        return (node_ip, True)  # Devuelve una tupla indicando éxito
                    else:
                        print(
                            f"Failed to send block to node {node_ip}. Status code: {response.status}"
                        )
            except Exception as e:
                print(f"Error sending block to node {node_ip}: {e}")

    # Leer el contenido del archivo
    # file_path = os.path.join(BLOCKCHAIN_DIR, filename)
    logging.info(f"Enviando el archivo {filename}")
    with open(filename, "rb") as file:
        block_data = file.read()

    # Obtener nodos activos
    active_nodes = await blc_sv.get_active_nodes(db)
    formatted_nodes = util_sv.convert_nodes(active_nodes)
    logging.info(f"formated_nodes:{formatted_nodes}")
    nodes = [{"ip": node["ip"]} for node in formatted_nodes]
    current_node = f"{IP}:{PORT}"
    # filtered_nodes = list(filter(lambda node: node["ip"] != current_node, nodes))
    logging.info(f"Todos los nodos activos:{nodes}")
    # Enviar el bloque a todos los nodos
    filename = filename.split("/")[1]
    tasks = [send_block_to_node(node["ip"], block_data, filename) for node in nodes]
    results = await asyncio.gather(*tasks)
    logging.info(f"results.....................................{results}")
    # Filtrar los resultados para eliminar `None`
    filtered_results = [(res[0], res[1]) for res in results if res is not None]

    # Contar éxitos y fracasos
    success_count = sum(1 for _, success in filtered_results if success)
    failure_count = sum(1 for _, success in filtered_results if not success)

    # Registrar los resultados para depuración
    logging.info(f"filtered_results: {filtered_results}")

    return {
        "status": "completed",
        "total_nodes": len(filtered_results),
        "successful_sends": success_count,
        "failed_sends": failure_count,
    }


# async def get_current_blocks_data(IP, PORT, NODE_ID, db):
#     active_nodes = await blc_sv.get_active_nodes(db)
#     formatted_nodes = util_sv.convert_nodes(active_nodes)
#     # Logging de nodos activos
#     logging.info("Nodos activos:")
#     for node in formatted_nodes:
#         ip, port = node["ip"].split(":")
#         logging.info(f"  - {ip}:{port}")

#     node_contacted = (
#         False  # Bandera para rastrear si se contactó con algún nodo exitoso
#     )

#     for node in formatted_nodes:
#         ip, port = node["ip"].split(":")
#         if await ping_node(ip, port):
#             logging.info(f"Nodo en {ip}:{port} ha respondido correctamente.")
#             logging.info("Solicitando información...")

#             block_count = len(os.listdir("BLOCKCHAIN/"))
#             url = f"http://{ip}:{port}/blockchain/sync/current_data"
#             params = {
#                 "blocknumber": block_count,
#             }

#             async with aiohttp.ClientSession() as session:
#                 try:
#                     async with session.get(url, params=params) as response:
#                         if response.status == 200:
#                             zip_content = await response.read()

#                             # Guardar el archivo zip recibido
#                             zip_filename = f"BLOCKCHAIN/sync_data_{NODE_ID}.zip"
#                             with open(zip_filename, "wb") as f:
#                                 f.write(zip_content)

#                             logging.info(
#                                 f"Archivo zip recibido y guardado como {zip_filename}."
#                             )

#                             # Descomprimir el archivo y guardar los bloques en la carpeta BLOCKCHAIN
#                             await compression_sv.unzip_file(zip_filename, "BLOCKCHAIN/")
#                             logging.info(
#                                 "Bloques sincronizados y añadidos a la carpeta BLOCKCHAIN."
#                             )

#                             # Eliminar el archivo zip una vez descomprimido
#                             os.remove(zip_filename)

#                         else:
#                             logging.error(
#                                 f"Error al obtener la data del nodo {ip}:{port}. Status: {response.status}"
#                             )
#                 except Exception as e:
#                     logging.error(
#                         f"Error en la solicitud al nodo {ip}:{port}. Error: {e}"
#                     )

#             # Marcar que se contactó con un nodo exitoso
#             node_contacted = True
#             # Salir del bucle después de contactar un nodo exitoso
#             break

#     if not node_contacted:
#         logging.error("No se ha podido contactar con ningún nodo.")


# async def get_current_database_data(ip, port, NODE_ID, db):
#     try:
#         # Obtener el bloque máximo registrado en la base de datos local
#         max_block_number_query = await db.execute(
#             _future.select([_sqlalchemy.func.max(blc_md.BLOQUES.numero_bloque)])
#         )
#         max_block_number = max_block_number_query.scalar()

#         if max_block_number is None:
#             max_block_number = 0  # Si no hay registros, comenzar desde 0

#         logging.info(
#             f"Máximo número de bloque en la base de datos local: {max_block_number}"
#         )

#         # URL para solicitar los registros de la base de datos desde el nodo
#         url = f"http://{ip}:{port}/blockchain/sync/current_database_data"
#         params = {"block_number_from": max_block_number}

#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, params=params) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     # Procesar y almacenar los datos de la base de datos sincronizados
#                     await db_sv.process_database_data(data, db)
#                 else:
#                     logging.error(
#                         f"Error en la solicitud a la base de datos del nodo {ip}:{port}. Status: {response.status}"
#                     )

#     except Exception as e:
#         logging.error(
#             f"Error en la solicitud a la base de datos del nodo {ip}:{port}. Error: {e}"
#         )


async def ping_node(ip, port):
    url = f"http://{ip}:{port}/ping"
    logging.info(f"Realizando ping al nodo {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return True
                else:
                    logging.warning(
                        f"El nodo en {ip}:{port} respondió con status {response.status}."
                    )
    except Exception as e:
        logging.warning(f"El nodo en {ip}:{port} no ha respondido.")
    return False


async def get_current_data(IP, PORT, NODE_ID, db):
    active_nodes = await blc_sv.get_active_nodes(db)
    formatted_nodes = util_sv.convert_nodes(active_nodes)

    # Logging de nodos activos
    if formatted_nodes:
        active_nodes = ", ".join([f"{node['ip']}" for node in formatted_nodes])
        logging.info(f"Nodos activos: {active_nodes}")
    else:
        logging.info("Nodos activos: 0")

    node_contacted = (
        False  # Bandera para rastrear si se contactó con algún nodo exitoso
    )

    for node in formatted_nodes:
        ip, port = node["ip"].split(":")
        if await ping_node(ip, port):
            logging.info(f"Nodo en {ip}:{port} ha respondido correctamente.")
            logging.info("Solicitando información...")

            # Llamar a get_current_block_data con el nodo activo
            await get_current_block_data(ip, port, NODE_ID, db)

            # Llamar a get_current_database_data con el nodo activo
            await get_current_database_data(ip, port, NODE_ID, db)

            # Marcar que se contactó con un nodo exitoso
            node_contacted = True
            # Salir del bucle después de contactar un nodo exitoso
            break

    if not node_contacted:
        logging.error("No se ha podido contactar con ningún nodo.")


async def get_current_block_data(ip: str, port: str, node_id: str, db: AsyncSession):
    block_count = len(os.listdir("BLOCKCHAIN/"))
    url = f"http://{ip}:{port}/blockchain/sync/current_data"
    params = {
        "blocknumber": block_count,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    zip_content = await response.read()
                    content_type = response.headers.get("Content-Type", "")

                    if "application/zip" in content_type:
                        zip_filename = f"sync_data_{node_id}.zip"
                        with open(zip_filename, "wb") as f:
                            f.write(zip_content)

                        logging.info(
                            f"Archivo zip recibido y guardado como {zip_filename}."
                        )

                        # Descomprimir el archivo y guardar los bloques en la carpeta BLOCKCHAIN
                        compression_sv.unzip_file(zip_filename, "BLOCKCHAIN/")
                        logging.info(
                            "Bloques sincronizados y añadidos a la carpeta BLOCKCHAIN."
                        )

                        # Eliminar el archivo zip una vez descomprimido
                        os.remove(zip_filename)
                    else:
                        json_content = await response.json()
                        logging.info(f"Respuesta JSON recibida: {json_content}")
                        # Procesar el contenido JSON aquí según lo necesario

                else:
                    logging.error(
                        f"Error al obtener la data del nodo {ip}:{port}. Status: {response.status}"
                    )
        except Exception as e:
            logging.error(f"Error en la solicitud al nodo {ip}:{port}. Error: {e}")


async def get_current_database_data(ip: str, port: str, node_id: str, db: _orm.Session):
    # Paso 1: Obtener el valor máximo de numero_bloque
    max_block_number = db.query(func.max(blc_md.BLOQUES.numero_bloque)).scalar()

    logging.info(
        f"Máximo número de bloque en la base de datos local: {max_block_number}"
    )
    # Paso 2: Realizar una petición al endpoint del nodo remoto
    url = f"http://{ip}:{port}/blockchain/sync/current_database_data"
    params = {"start_block": max_block_number + 1}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    logging.info(f"Datos recibidos desde el nodo {ip}:{port}")
    logging.info(data)
    # Paso 3: Insertar los registros recibidos en la base de datos local
    if "data" in data:
        blocks = data["data"]
        # Insertar los registros en la base de datos local
        for block in blocks:
            # La estructura de `block` debe ser un diccionario
            # Aquí asumimos que la clave del diccionario es 'BLOQUES', ajusta según sea necesario
            block_data = block.get("BLOQUES")
            if block_data:
                # Crear una instancia del modelo BLOQUES
                new_block = blc_md.BLOQUES(
                    id_bloque=block_data["id_bloque"],
                    fecha_inicio=block_data["fecha_inicio"],
                    fecha_fin=block_data["fecha_fin"],
                    id_evento=block_data["id_evento"],
                    org=block_data["org"],
                    creador=block_data["creador"],
                    path=block_data["path"],
                    timestamp=block_data["timestamp"],
                    numero_bloque=block_data["numero_bloque"],
                )
                db.add(new_block)
        db.commit()
        logging.info(f"Registros insertados correctamente.")
    else:
        logging.warning("No se encontraron datos en la respuesta del nodo.")
