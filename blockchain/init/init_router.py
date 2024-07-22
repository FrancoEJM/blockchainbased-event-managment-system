import os
import json
import requests
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from models import blc_models as blc_md
from services import database_services as db_sv

router = _fastapi.APIRouter()


@router.post("/receive-sync-data")
async def receive_sync_data(data, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        files = data.get("files", [])
        bloques = data.get("bloques", [])
        nodos = data.get("nodos", [])

        # Guardar archivos en la carpeta /BLOCKCHAIN
        blockchain_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../BLOCKCHAIN")
        )
        os.makedirs(blockchain_folder, exist_ok=True)
        for file in files:
            filename = file["filename"]
            file_data = file["data"]
            filepath = os.path.join(blockchain_folder, filename)
            with open(filepath, "w") as f:
                f.write(file_data)

        # Guardar datos en la base de datos
        for bloque in bloques:
            new_bloque = blc_md.BLOQUES(**bloque)
            db.add(new_bloque)

        for nodo in nodos:
            new_nodo = blc_md.NODOS(**nodo)
            db.add(new_nodo)

        db.commit()

        return {"message": "Data received successfully"}
    except Exception as e:
        return {"message": "Error occurred", "error": str(e)}


@router.get("/full-sync")
async def send_all_data(
    ip: str, port: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    # Recolectar todos los archivos .txt de la carpeta /BLOCKCHAIN
    blockchain_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../BLOCKCHAIN")
    )

    files_data = []
    for filename in os.listdir(blockchain_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(blockchain_folder, filename)
            with open(filepath, "r") as file:
                file_data = file.read()
            files_data.append({"filename": filename, "data": file_data})
    # Recolectar datos de las tablas BLC_BLOQUE y BLC_NODO
    bloques = db.query(blc_md.BLOQUES).all()
    nodos = db.query(blc_md.NODOS).all()

    bloques_data = [
        {
            "id_bloque": b.id_bloque,
            "fecha_inicio": b.fecha_inicio.isoformat() if b.fecha_inicio else None,
            "fecha_fin": b.fecha_fin.isoformat() if b.fecha_fin else None,
            "id_evento": b.id_evento,
            "org": b.org,
            "creador": b.creador,
            "path": b.path,
        }
        for b in bloques
    ]

    nodos_data = [
        {
            "id_nodo": n.id_nodo,
            "fecha_creacion": n.fecha_creacion.isoformat()
            if n.fecha_creacion
            else None,
            "status": n.status,
            "organizacion": n.organizacion,
            "ip": n.ip,
            "port": n.port,
        }
        for n in nodos
    ]

    # Crear el paquete de datos
    data_package = {"files": files_data, "bloques": bloques_data, "nodos": nodos_data}
    print("-------------------")
    print("data_package", data_package)
    print("-------------------")

    # Serializar el paquete de datos para verificar su contenido
    try:
        data_package_serialized = json.dumps(data_package)
        print("Serialized data_package:", data_package_serialized)
    except TypeError as e:
        print("Failed to serialize data_package:", e)
        return {"message": "Serialization error", "error": str(e)}

    # Enviar los datos al nodo especificado por IP y puerto
    try:
        url = f"http://{ip}:{port}/receive-sync-data"
        print("-------------------")
        print("url", url)
        print("-------------------")
        headers = {"Content-Type": "application/json"}
        print("-------------------")
        print("data", data_package_serialized)
        print("-------------------")
        response = requests.post(url, headers=headers, data=data_package_serialized)
        if response.status_code == 200:
            return {"message": "Data sent successfully"}
        else:
            return {
                "message": "Failed to send data",
                "status_code": response.status_code,
                "response": response.text,  # Include response text for more debugging information
            }
    except Exception as e:
        return {"message": "Error occurred", "error": str(e)}
