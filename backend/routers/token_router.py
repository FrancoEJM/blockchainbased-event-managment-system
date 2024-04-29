import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv

router = _fastapi.APIRouter()

@router.post("/api/token")
async def generate_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
                         db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    user = await user_sv.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
                                     detail="Credenciales incorrectas")
    
    return await token_sv.create_token(user)