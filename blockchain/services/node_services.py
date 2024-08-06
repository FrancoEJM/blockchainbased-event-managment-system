import sqlalchemy.orm as _orm
from models import blockchain_models as blc_md


async def record_node_data(node_id: int, waited_time: int, db: _orm.Session):
    try:
        node = db.query(blc_md.NODOS).filter_by(id_nodo=node_id).first()

        if node:
            node.tiempo_esperado += waited_time

            db.commit()
            db.refresh(node)
            print(f"Tiempo esperado actualizado correctamente para el nodo {node_id}.")
        else:
            print(f"Nodo con id {node_id} no encontrado.")

    except Exception as e:
        print(f"Error al actualizar el nodo: {e}")
        db.rollback()
