import qrcode
import sqlalchemy.orm as _orm
from models import event_models as event_md


async def generate_user_qr(event_id: int, email: str, token: str, db: _orm.Session):
    print("INICIOOOOOOOOOOOOOOO")
    print("INICIOOOOOOOOOOOOOOO")
    print("INICIOOOOOOOOOOOOOOO")
    print("INICIOOOOOOOOOOOOOOO")
    print("INICIOOOOOOOOOOOOOOO")
    qr_data = {"event_id": event_id, "email": email, "token": token}
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_path = f"data/userPrivateQRImages/{event_id}_{email.split('@')[0]}.png"
    qr_img.save(qr_img_path)

    existing_qr = (
        db.query(event_md.EventosQRPrivados)
        .filter_by(id_evento=event_id, correo_electronico=email)
        .first()
    )

    if existing_qr:
        existing_qr.path_qr = qr_img_path
    else:
        new_qr = event_md.EventosQRPrivados(
            id_evento=event_id, correo_electronico=email, path=qr_img_path, token=token
        )
        db.add(new_qr)

    db.commit()
    print("TERMINOOOOO")
    print("TERMINOOOOO")
    print("TERMINOOOOO")
    print("TERMINOOOOO")
