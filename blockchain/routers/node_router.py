import fastapi as _fastapi
from services import (
    blockchain_services as blc_sv,
    database_services as db_sv,
    block_services as block_sv,
    node_services as node_sv,
)
from models import blockchain_models as blc_md
import sqlalchemy.orm as _orm
import typing as _typing
import logging

router = _fastapi.APIRouter()


@router.post("/blockchain/nodes/waited_times")
async def update_waited_times(
    assigned_data: _typing.List[dict], db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    try:
        for node_data in assigned_data:
            node_id = node_data.get("node_id")
            assigned_time = node_data.get("assigned_time")

            # Buscar el nodo en la base de datos
            db_node = (
                db.query(blc_md.NODOS).filter(blc_md.NODOS.id_nodo == node_id).first()
            )
            if db_node:
                # Actualizar el tiempo esperado
                db_node.tiempo_esperado += assigned_time
                db.commit()

                # Registrar la asignación en la consola
                logging.info(
                    f"Tiempo asignado {assigned_time} para el nodo {node_id}. Nuevo tiempo esperado: {db_node.tiempo_esperado}"
                )

        return {"status": "success", "message": "Tiempos actualizados correctamente"}
    except Exception as e:
        db.rollback()
        raise _fastapi.HTTPException(
            status_code=500, detail=f"Error actualizando los tiempos: {str(e)}"
        )


@router.get("/blockchain/nodes")
async def get_events_list(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    return await blc_sv.get_active_nodes(db)
