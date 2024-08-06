import fastapi as _fastapi
import sqlalchemy.orm as _orm

from services import database_services as db_sv, transaction_services as tx_sv

router = _fastapi.APIRouter()


@router.post("/transactions/validate")
async def validate_transactions(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    digital_signature = tx_sv.check_digital_signature()
    if digital_signature:
        pass
