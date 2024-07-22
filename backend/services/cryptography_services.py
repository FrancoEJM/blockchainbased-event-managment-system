import os
import json as json_lib
import sqlalchemy.orm as _orm
from models import user_models as user_md
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


# Clave Fernet para encriptación
FERNET_KEY = os.getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY)


async def create_cryptographic_credentials(user_id: int, db: _orm.Session):
    private_key, public_key = await create_key_pair()
    await save_key_pair(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ),
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
        user_id,
        db,
    )


async def create_key_pair():
    # Generar la clave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Obtener la clave pública correspondiente
    public_key = private_key.public_key()

    return private_key, public_key


async def save_key_pair(private_key, public_key, user_id, db: _orm.Session):
    try:
        # Encriptar las claves con Fernet
        encrypted_private_key = fernet.encrypt(private_key)
        encrypted_public_key = fernet.encrypt(public_key)

        # Buscar al user_obj por user_id
        user_obj = (
            db.query(user_md.Usuario)
            .filter(user_md.Usuario.id_usuario == user_id)
            .first()
        )

        if user_obj:
            # Actualizar las claves encriptadas en el user_obj
            user_obj.llave_privada = encrypted_private_key
            user_obj.llave_publica = encrypted_public_key

            db.commit()
            print(f"Claves encriptadas y guardadas para el usuario con id {user_id}")
        else:
            print(f"No se encontró ningún usuario con id {user_id}")

    except Exception as e:
        print(f"Error al guardar las claves en la base de datos: {str(e)}")
        db.rollback()


async def get_keys(user_id: int, db: _orm.Session):
    usuario = (
        db.query(user_md.Usuario).filter(user_md.Usuario.id_usuario == user_id).first()
    )
    if usuario and usuario.llave_publica and usuario.llave_privada:
        fernet = Fernet(FERNET_KEY.encode())
        public_key = fernet.decrypt(usuario.llave_publica).decode()
        private_key = fernet.decrypt(usuario.llave_privada).decode()
        return public_key, private_key
    return None


async def digital_signature(private_key, transactions):
    json_data = json_lib.dumps(transactions, indent=4)
    print(json_data)
    # Convertir transacciones a JSON
    transactions_json = json_lib.dumps(transactions, separators=(",", ":")).encode(
        "utf-8"
    )

    # Cargar la clave privada desde el PEM
    private_key = serialization.load_pem_private_key(
        private_key.encode(), password=None
    )

    # Firmar el JSON de las transacciones
    signature = private_key.sign(
        transactions_json,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256(),
    )

    return signature.hex()
