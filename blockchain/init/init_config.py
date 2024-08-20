import csv
import time
import random
import requests
import subprocess
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models import blockchain_models as blc_md


def create_tables(database_url):
    try:
        # Crear el motor de SQLAlchemy
        engine = create_engine(database_url)

        # Crear las tablas en la base de datos
        blc_md.Base.metadata.create_all(engine)
        print("Tablas creadas exitosamente.")

    except SQLAlchemyError as e:
        # Manejo de errores en caso de que no se puedan crear las tablas
        print(f"Error al crear las tablas: {e}")
        raise  # Lanzar la excepción para detener el programa


def create_dotenv_file(ip, port, database_url):
    with open(".env", "w") as f:
        f.write(f"IP={ip}\n")
        f.write(f"PORT={port}\n")
        f.write(f"DATABASE_URL={database_url}\n")


def start_uvicorn(ip, port):
    # Inicia el servidor Uvicorn en un proceso separado
    process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", ip, "--port", str(port)]
    )
    # Espera unos segundos para asegurarse de que el servidor esté activo
    time.sleep(5)
    return process


def stop_uvicorn(process):
    # Termina el proceso de Uvicorn
    process.terminate()


def add_node_to_network(blc_config_file, org_config_file):
    # Leer el archivo CSV de configuración de la organización
    with open(org_config_file, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        org_config = next(csv_reader)
        ip = org_config["ip"]
        port = org_config["port"]
        database = org_config["database_url"]

    # Generar el archivo .env con la IP y el puerto
    create_dotenv_file(ip, port, database)

    # Crear tablas
    create_tables(database)
    # Encontrar el nodo activo (esta parte de la función no se proporciona)
    active_node = find_running_node(blc_config_file)
    if not active_node:
        print("No active node found.")
        return

    uvicorn_process = start_uvicorn(ip, port)

    # Enviar la petición al nodo activo
    url = f"http://{active_node['ip']}:{active_node['port']}/full-sync"
    try:
        response = requests.get(url, params={"ip": ip, "port": port})
        print("response en add_node_to_network", response.json())
    except requests.exceptions.RequestException as e:
        print(e)
    finally:
        # Detener el servidor Uvicorn
        stop_uvicorn(uvicorn_process)


def find_running_node(blc_config_file):
    # Leer archivo de configuración de la blockchain
    blockchain_nodes = []
    with open(blc_config_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            blockchain_nodes.append(row)

    random.shuffle(blockchain_nodes)
    # Intentamos conectar con un nodo activo de la red,
    for node in blockchain_nodes:
        active_node = node
        url = f"http://{node['ip']}:{node['port']}/ping"
        try:
            print(f"Intentando conectar con {node['ip']}:{node['port']}")
            response = requests.get(url)
            if response.status_code == 200:
                print(f"El nodo {node['ip']}:{node['port']} está encendido.")
                return active_node
        except requests.exceptions.RequestException:
            print("Sin respuesta. Intentando siguiente nodo...")
        sleep(1)

    # Si ningún nodo responde
    print("No existen nodos activos en la red, por favor contacte con el administrador")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Procesa dos archivos de configuración."
    )
    parser.add_argument(
        "blc_config",
        metavar="blc_config_file",
        type=str,
        help="Nombre del archivo de configuración de la blockchain",
    )
    parser.add_argument(
        "org_config",
        metavar="org_config_file",
        type=str,
        help="Nombre del archivo de configuración de la organización",
    )

    args = parser.parse_args()

    add_node_to_network(args.blc_config, args.org_config)
