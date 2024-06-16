import fastapi as _fastapi
import fastapi.responses as _responses
import sqlalchemy.orm as _orm

from schemas import user_schemas as user_sch
from services import database_services as db_sv, user_services as user_sv

router = _fastapi.APIRouter()


@router.post("/api/users")
async def create_user(
    user: user_sch.UserCreate, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    db_user = await user_sv.get_user_by_email(user.correo_electronico, db)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico está en uso",
        )
    return await user_sv.create_user(user, db)


@router.get("/api/users/me", response_model=user_sch.User)
async def get_user(user: user_sch.User = _fastapi.Depends(user_sv.get_current_user)):
    return user


@router.post("/api/user/unregistered_details")
async def save_attendee_data(
    details: user_sch.AttendeeDetails, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    return await user_sv.save_attendee_data(
        details.event_id, details.gender, details.fullname, details.birthdate, db
    )


@router.post("/api/user/validate_by_qr", status_code=_fastapi.status.HTTP_202_ACCEPTED)
async def validate_user_by_qr(
    event_id: int,
    email: str,
    token: str,
    db: _orm.Session = _fastapi.Depends(db_sv.get_db),
):
    invitation = await user_sv.is_invited(event_id, email, token, db)
    if invitation:
        return invitation
    raise _fastapi.HTTPException(
        status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="El usuario no ha sido invitado o ya ha ingresado al evento",
    )
