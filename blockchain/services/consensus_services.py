import sqlalchemy.orm as _orm

from services import blockchain_services as blc_sv
from models import blc_models as blc_md

from typing import List
import random
import asyncio
import httpx
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


async def send_poet_request(node):
    assigned_time = node["assigned_time"]
    ip = node["ip"]

    async with httpx.AsyncClient() as client:
        start_time = time.time()
        response = await client.post(
            f"http://{ip}/poet-wait", json={"assigned_time": assigned_time}
        )
        end_time = time.time()
        real_waited_time = end_time - start_time
        response_data = response.json()
        return {
            "ip": ip,
            "assigned_time": assigned_time,
            "real_waited_time": real_waited_time,
            "response_data": response_data,
        }


async def proof_of_elapsed_time(nodes, epsilon):
    # Generar tiempos de espera
    assigned_data = assign_times(nodes, epsilon)
    # Realizar llamadas concurrentes a los nodos activos de la red con su tiempo de espera
    responses = await asyncio.gather(
        *[send_poet_request(node) for node in assigned_data]
    )

    # Ordenar las respuestas por el tiempo de espera real
    sorted_responses = sorted(responses, key=lambda x: x["real_waited_time"])

    # Imprimir todas las respuestas
    for response in sorted_responses:
        print(
            f"assigned_time nodo {response['ip']}: {response['assigned_time']}, "
            f"real_time nodo {response['ip']} : {response['real_waited_time']}"
        )

    return sorted_responses
