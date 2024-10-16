import os
import json
import requests
import fastapi as _fastapi
import sqlalchemy.orm as _orm
from models import blockchain_models as blc_md
from services import database_services as db_sv
import logging
import datetime as _dt
import sqlalchemy as _sql
import zipfile
import io

router = _fastapi.APIRouter()


# @router.post("/blockchain/node")
# async def registry_new_node(
#     data: dict, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
# ):
#     logging.info(data)

#     # Calcular el tiempo esperado promedio de los nodos existentes
#     total_tiempo_esperado = db.query(
#         _sql.func.sum(blc_md.NODOS.tiempo_esperado)
#     ).scalar()
#     total_nodos = db.query(_sql.func.count(blc_md.NODOS.id_nodo)).scalar()
#     logging.info(f"total_nodos:{total_nodos}")
#     if total_nodos > 0:
#         promedio_tiempo_esperado = total_tiempo_esperado / total_nodos
#     else:
#         promedio_tiempo_esperado = 0  # En caso de que no haya nodos, establecer en 0

#     now = _dt.datetime.now(_dt.timezone.utc)
#     # Crear un nuevo nodo con la información proporcionada en 'data'
#     new_node = blc_md.NODOS(
#         id_nodo=total_nodos + 1,
#         ip=data["ip"],
#         port=int(data["port"]),  # Asegúrate de convertir el puerto a entero
#         organizacion=data["organization"],
#         status=True,  # Establecer el estado como True
#         tiempo_esperado=promedio_tiempo_esperado,  # Establecer el tiempo esperado promedio
#         fecha_creacion=now,  # Establecer la fecha de creación actual
#     )

#     # Agregar el nuevo nodo a la sesión de la base de datos
#     db.add(new_node)

#     # Confirmar los cambios en la base de datos
#     db.commit()

#     # Obtener el ID del nuevo nodo
#     new_node_id = new_node.id_nodo


#     return {
#         "message": "Node registered successfully",
#         "id": new_node_id,
#         "waited_time": promedio_tiempo_esperado,
#         "created_at": now,
#     }
@router.post("/blockchain/node", status_code=201)
async def add_node(
    request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    try:
        # Obtener los datos del cuerpo de la solicitud
        node_data = await request.json()

        # Validación básica de los campos requeridos
        required_fields = [
            "id_nodo",
            "fecha_creacion",
            "tiempo_esperado",
            "status",
            "organizacion",
            "ip",
            "port",
        ]
        for field in required_fields:
            if field not in node_data:
                raise _fastapi.HTTPException(
                    status_code=400, detail=f"Falta el campo requerido: {field}"
                )

        # Verificar si el nodo ya existe en la base de datos por IP y puerto
        existing_node = (
            db.query(blc_md.NODOS)
            .filter(
                blc_md.NODOS.ip == node_data["ip"],
                blc_md.NODOS.port == node_data["port"],
            )
            .first()
        )

        if existing_node:
            raise _fastapi.HTTPException(
                status_code=400, detail="El nodo ya existe en la base de datos."
            )

        # Crear el nuevo nodo
        new_node = blc_md.NODOS(
            id_nodo=node_data["id_nodo"],
            fecha_creacion=_dt.datetime.strptime(
                node_data["fecha_creacion"], "%Y-%m-%dT%H:%M:%S"
            ),
            tiempo_esperado=node_data["tiempo_esperado"],
            status=node_data["status"],
            organizacion=node_data["organizacion"],
            ip=node_data["ip"],
            port=node_data["port"],
        )

        # Insertar el nodo en la base de datos
        db.add(new_node)
        db.commit()
        db.refresh(new_node)

        return {"status": "Nodo añadido con éxito", "nodo_id": new_node.id_nodo}
    except Exception as e:
        db.rollback()
        raise _fastapi.HTTPException(
            status_code=500, detail=f"Error al añadir el nodo: {str(e)}"
        )


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


# @router.get("/full-sync")
# async def send_all_data(
#     ip: str, port: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
# ):
#     # Recolectar todos los archivos .txt de la carpeta /BLOCKCHAIN
#     blockchain_folder = os.path.abspath(
#         os.path.join(os.path.dirname(__file__), "../BLOCKCHAIN")
#     )

#     files_data = []
#     for filename in os.listdir(blockchain_folder):
#         if filename.endswith(".zip"):
#             filepath = os.path.join(blockchain_folder, filename)
#             with open(filepath, "r", encoding="utf-8") as file:
#                 file_data = file.read()
#             files_data.append({"filename": filename, "data": file_data})
#     # Recolectar datos de las tablas BLC_BLOQUE y BLC_NODO
#     bloques = db.query(blc_md.BLOQUES).all()
#     nodos = db.query(blc_md.NODOS).all()

#     bloques_data = [
#         {
#             "id_bloque": b.id_bloque,
#             "fecha_inicio": b.fecha_inicio.isoformat() if b.fecha_inicio else None,
#             "fecha_fin": b.fecha_fin.isoformat() if b.fecha_fin else None,
#             "id_evento": b.id_evento,
#             "org": b.org,
#             "creador": b.creador,
#             "path": b.path,
#         }
#         for b in bloques
#     ]

#     nodos_data = [
#         {
#             "id_nodo": n.id_nodo,
#             "fecha_creacion": n.fecha_creacion.isoformat()
#             if n.fecha_creacion
#             else None,
#             "status": n.status,
#             "organizacion": n.organizacion,
#             "ip": n.ip,
#             "port": n.port,
#         }
#         for n in nodos
#     ]

#     # Crear el paquete de datos
#     data_package = {"files": files_data, "bloques": bloques_data, "nodos": nodos_data}
#     print("-------------------")
#     print("data_package", data_package)
#     print("-------------------")

#     # Serializar el paquete de datos para verificar su contenido
#     try:
#         data_package_serialized = json.dumps(data_package)
#         print("Serialized data_package:", data_package_serialized)
#     except TypeError as e:
#         print("Failed to serialize data_package:", e)
#         return {"message": "Serialization error", "error": str(e)}

#     # Enviar los datos al nodo especificado por IP y puerto
#     try:
#         url = f"http://{ip}:{port}/receive-sync-data"
#         print("-------------------")
#         print("url", url)
#         print("-------------------")
#         headers = {"Content-Type": "application/json"}
#         print("-------------------")
#         print("data", data_package_serialized)
#         print("-------------------")
#         response = requests.post(url, headers=headers, data=data_package_serialized)
#         if response.status_code == 200:
#             return {"message": "Data sent successfully"}
#         else:
#             return {
#                 "message": "Failed to send data",
#                 "status_code": response.status_code,
#                 "response": response.text,  # Include response text for more debugging information
#             }
#     except Exception as e:
#         return {"message": "Error occurred", "error": str(e)}


def get_data(db: _orm.Session):
    try:
        # Recolectar datos de la base de datos
        bloques = db.query(blc_md.BLOQUES).all()
        nodos = db.query(blc_md.NODOS).all()

        # Crear un archivo .zip en memoria
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            # Convertir datos de BLOQUES a JSON y agregar al archivo .zip
            bloques_data = [
                b.to_dict() for b in bloques
            ]  # Asegúrate de tener un método to_dict en BLOQUES
            zip_file.writestr("bloques.json", json.dumps(bloques_data, indent=4))

            # Convertir datos de NODOS a JSON y agregar al archivo .zip
            nodos_data = [
                n.to_dict() for n in nodos
            ]  # Asegúrate de tener un método to_dict en NODOS
            zip_file.writestr("nodos.json", json.dumps(nodos_data, indent=4))

        buffer.seek(0)
        return buffer
    finally:
        db.close()


def collect_blockchain_files():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_file:
        blockchain_folder = "BLOCKCHAIN/"
        for root, dirs, files in os.walk(blockchain_folder):
            for file in files:
                if file.endswith(".zip"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        zip_file.writestr(file, f.read())
    buffer.seek(0)
    return buffer


@router.get("/full-sync")
async def full_sync(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        # Recolectar datos de la base de datos
        db_data = get_data(db)

        # Recolectar archivos de la carpeta BLOCKCHAIN/
        blockchain_files = collect_blockchain_files()

        # Crear un archivo .zip en memoria
        final_buffer = io.BytesIO()
        with zipfile.ZipFile(final_buffer, "w") as final_zip:
            # Agregar datos de la base de datos
            db_data.seek(0)
            with zipfile.ZipFile(db_data, "r") as db_zip:
                for file_info in db_zip.infolist():
                    final_zip.writestr(
                        file_info.filename, db_zip.read(file_info.filename)
                    )

            # Agregar archivos de la carpeta BLOCKCHAIN/
            blockchain_files.seek(0)
            with zipfile.ZipFile(blockchain_files, "r") as blockchain_zip:
                for file_info in blockchain_zip.infolist():
                    final_zip.writestr(
                        file_info.filename, blockchain_zip.read(file_info.filename)
                    )

        final_buffer.seek(0)
        return _fastapi.responses.StreamingResponse(
            final_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=full_sync_data.zip"},
        )
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=str(e))
