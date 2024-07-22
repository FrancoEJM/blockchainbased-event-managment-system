import fastapi as _fastapi
import sqlalchemy.orm as _orm
from services import (
    database_services as db_sv,
    blockchain_services as blc_sv,
    consensus_services as consensus_sv,
    util_services as util_sv,
)
from models import blc_models as blc_md
from typing import List, Dict

router = _fastapi.APIRouter()


@router.post("/blockchain/process-transactions")
async def process_transactions(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    active_nodes = await blc_sv.get_active_nodes(db)
    formatted_nodes = util_sv.convert_nodes(active_nodes)
    selected_node = await consensus_sv.proof_of_elapsed_time(formatted_nodes, 8)
    return selected_node


@router.get("/api/nodes")
async def get_events_list(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    return await blc_sv.get_active_nodes(db)
