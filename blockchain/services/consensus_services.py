import sqlalchemy.orm as _orm

from services import blockchain_services as blc_sv
from models import blockchain_models as blc_md

from typing import List
import random
import asyncio
import httpx
import aiohttp
import time


# Con 1 <= epsilon <= 10
# epsilon bajo, asignación aleatoria.
# epsilon alto, el nodo con mayor tiempo de espera tiene mayor probabilidad de obtener un tiempo bajo.
def assign_times(nodes, epsilon):
    # Número de nodos
    n = len(nodes)

    # Generar tiempos aleatorios en el rango [2, 10]
    times = [random.uniform(2, 10) for _ in range(n)]

    # Normalizar el tiempo esperado
    total_tiempo_esperado = sum(node["tiempo_esperado"] for node in nodes)
    base_probabilities = [
        node["tiempo_esperado"] / total_tiempo_esperado for node in nodes
    ]

    # Calcular probabilidades ajustadas
    adjusted_probabilities = []
    for i in range(n):
        adjusted_probability = (1 - epsilon / 10) * (1 / times[i]) + (
            epsilon / 10
        ) * base_probabilities[i]
        adjusted_probabilities.append(adjusted_probability)

    # Normalizar las probabilidades
    total_adjusted_prob = sum(adjusted_probabilities)
    normalized_probabilities = [
        prob / total_adjusted_prob for prob in adjusted_probabilities
    ]

    # Asignar tiempos a nodos basados en probabilidades
    sorted_indices = sorted(range(n), key=lambda i: normalized_probabilities[i])
    assigned_times = [0] * n
    for i, idx in enumerate(sorted_indices):
        assigned_times[idx] = times[i]

    # Crear resultado con tiempos asignados
    result = [
        {
            "ip": nodes[i]["ip"],
            "tiempo_esperado": nodes[i]["tiempo_esperado"],
            "assigned_time": assigned_times[i],
        }
        for i in range(n)
    ]

    return result


# async def send_poet_request(node):
#     assigned_time = node["assigned_time"]
#     ip = node["ip"]
#     client_timestamp = time.time()

#     async with httpx.AsyncClient() as client:
#         start_time = time.time()
#         response = await client.post(
#             f"http://{ip}/poet-wait",
#             json={"assigned_time": assigned_time, "timestamp": client_timestamp},
#         )
#         end_time = time.time()
#         response_data = response.json()
#         real_waited_time = end_time - start_time
#         round_trip_time = end_time - client_timestamp
#         processing_time = (
#             response_data["server_timestamp"] - client_timestamp - assigned_time
#         )
#         return {
#             "ip": ip,
#             "assigned_time": assigned_time,
#             "real_waited_time": real_waited_time,
#             "round_trip_time": round_trip_time,
#             "processing_time": processing_time,
#             "response_data": response_data,
#         }


async def send_poet_request(node):
    timeout = aiohttp.ClientTimeout(
        total=20,  # Tiempo total máximo de espera en segundos
        connect=10,  # Tiempo máximo de conexión en segundos
        sock_connect=5,  # Tiempo máximo para conectar al socket en segundos
        sock_read=10,  # Tiempo máximo para leer desde el socket en segundos
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = f"http://{node['ip']}/poet-wait"
        client_timestamp = time.time()
        payload = {
            "assigned_time": node["assigned_time"],
            "timestamp": client_timestamp,
        }
        try:
            async with session.post(url, json=payload) as response:
                response.raise_for_status()  # Lanzar una excepción para códigos de estado HTTP 4xx/5xx
                response_data = await response.json()
                server_timestamp = response_data.get("server_timestamp", time.time())
                # Calculamos los tiempos
                real_waited_time = server_timestamp - client_timestamp
                round_trip_time = time.time() - client_timestamp
                processing_time = (
                    server_timestamp - client_timestamp - node["assigned_time"]
                )

                return {
                    "ip": node["ip"],
                    "assigned_time": node["assigned_time"],
                    "real_waited_time": real_waited_time,
                    "round_trip_time": round_trip_time,
                    "processing_time": processing_time,
                    "response_data": response_data,
                }
        except Exception as e:
            # Manejar la excepción y retornar None o un diccionario con un estado de error
            print(f"Error al contactar al nodo {node['ip']}: {str(e)}")
            return {
                "ip": node["ip"],
                "assigned_time": node["assigned_time"],
                "real_waited_time": float(
                    "inf"
                ),  # Valores altos para asegurar que no sean seleccionados
                "round_trip_time": float("inf"),
                "processing_time": float("inf"),
                "response_data": {"error": str(e)},
            }


async def proof_of_elapsed_time(nodes, epsilon):
    assigned_data = assign_times(nodes, epsilon)
    responses = await asyncio.gather(
        *[send_poet_request(node) for node in assigned_data]
    )

    # Filtrar las respuestas que tuvieron éxito
    valid_responses = [
        response
        for response in responses
        if response["real_waited_time"] != float("inf")
    ]

    if not valid_responses:
        raise Exception("No se pudo contactar a ningún nodo exitosamente.")

    sorted_responses = sorted(valid_responses, key=lambda x: x["real_waited_time"])

    return sorted_responses[0]
