from services import blockchain_services as blc_sv
import sqlalchemy.orm as _orm
import aiohttp
import asyncio
import logging


async def notify_status_change(id: int, status: bool, db: _orm.Session):
    active_nodes = await blc_sv.get_active_nodes(db)
    nodes_to_notify = [node for node in active_nodes if node.id_nodo != id]
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
