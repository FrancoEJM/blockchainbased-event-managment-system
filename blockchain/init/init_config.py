import csv
import time
import random
import requests
import subprocess
from time import sleep
from sqlalchemy import create_engine, func
from sqlalchemy.exc import SQLAlchemyError

import sqlalchemy.orm as _orm
import logging
import datetime as _dt
import sys
import os
import zipfile
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models import blockchain_models as blc_md

from services import (
    database_services as db_sv,
    util_services as util_sv,
    blockchain_services as blc_sv,
)


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
        raise e  # Lanzar la excepción para detener el programa


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
        org = org_config["organization"]

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
    blockchain_dir = "BLOCKCHAIN"
    zip_path = os.path.join(blockchain_dir, "full_sync_data.zip")
    bloques_file = os.path.join(blockchain_dir, "bloques.json")
    nodos_file = os.path.join(blockchain_dir, "nodos.json")
    # Enviar la petición al nodo activo
    url = f"http://{active_node['ip']}:{active_node['port']}/full-sync"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Guardar el archivo .zip en la carpeta BLOCKCHAIN

            os.makedirs(blockchain_dir, exist_ok=True)
            with open(zip_path, "wb") as f:
                f.write(response.content)

            # Extraer archivos JSON del archivo .zip
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(blockchain_dir)

            # Leer y procesar archivos JSON
            process_json_files(blockchain_dir, database)

            # Obtener el id_nodo, fecha_creacion, tiempo_esperado y status
            db_session = db_sv.get_db()
            id_nodo = db_session.query(blc_md.NODOS).count() + 1
            fecha_creacion = _dt.datetime.now()
            tiempo_esperado = (
                db_session.query(func.avg(blc_md.NODOS.tiempo_esperado)).scalar() or 0
            )  # Promedio o 0 si no hay registros
            status = True

            # Crear un nuevo nodo en la base de datos local
            nuevo_nodo = blc_md.NODOS(
                id_nodo=id_nodo,
                fecha_creacion=fecha_creacion,
                tiempo_esperado=tiempo_esperado,
                status=status,
                organizacion=org,
                ip=ip,
                port=port,
            )
            db_session.add(nuevo_nodo)
            db_session.commit()

            # Preparar datos del nodo para enviar a los nodos activos de la red
            node_data = {
                "id_nodo": id_nodo,
                "fecha_creacion": fecha_creacion.isoformat(),
                "tiempo_esperado": tiempo_esperado,
                "status": status,
                "organizacion": org,
                "ip": ip,
                "port": port,
            }

            # Registrar el nodo en todos los nodos activos de la red
            active_nodes = blc_sv.get_active_nodes(db_session)
            formatted_nodes = util_sv.convert_nodes(active_nodes)
            for node in formatted_nodes:
                try:
                    remote_url = f"http://{node['ip']}/blockchain/node"
                    remote_response = requests.post(remote_url, json=node_data)
                    if remote_response.status_code == 200:
                        print(f"Nodo registrado en {node['ip']} con éxito")
                    else:
                        print(
                            f"Error al registrar nodo en {node['ip']}: {remote_response.status_code}"
                        )
                except requests.exceptions.RequestException as e:
                    print(f"Error en la solicitud a {node['ip']}: {e}")
        else:
            print(f"Error en la respuesta del nodo: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    finally:
        # Detener el servidor Uvicorn
        stop_uvicorn(uvicorn_process)
        # Eliminar los archivos recibidos
        for file_path in [zip_path, bloques_file, nodos_file]:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Eliminado {file_path}")


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


def process_json_files(directory, database_url):
    # Conectar a la base de datos
    engine = create_engine(database_url)
    SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        # Procesar archivo bloques.json
        bloques_file = os.path.join(directory, "bloques.json")
        if os.path.exists(bloques_file):
            with open(bloques_file, "r") as f:
                bloques_data = json.load(f)
                for bloque in bloques_data:
                    db.add(blc_md.BLOQUES(**bloque))
                db.commit()

        # Procesar archivo nodos.json
        nodos_file = os.path.join(directory, "nodos.json")
        if os.path.exists(nodos_file):
            with open(nodos_file, "r") as f:
                nodos_data = json.load(f)
                for nodo in nodos_data:
                    db.add(blc_md.NODOS(**nodo))
                db.commit()


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
