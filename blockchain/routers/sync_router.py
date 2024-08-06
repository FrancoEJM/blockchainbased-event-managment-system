import fastapi as _fastapi
import sqlalchemy.orm as _orm
from services import database_services as db_sv
from models import blockchain_models as blc_md

router = _fastapi.APIRouter()


@router.post("/nodes/{node_id}/update_status")
async def update_status(
    node_id: int, status: bool, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    node = db.query(blc_md.NODOS).filter(blc_md.NODOS.id_nodo == node_id).first()
    if node:
        node.status = status
        db.commit()
        return {"message": "Node status updated successfully"}
    else:
        raise _fastapi.HTTPException(status_code=404, detail="Node not found")
