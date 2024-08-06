import os
import hashlib
import json as json_lib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# Función para calcular el hash del bloque
async def calculate_block_hash(block_data: dict) -> str:
    block_string = json_lib.dumps(block_data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(block_string).hexdigest()


async def check_digital_signature(event_data):
    try:
        # Convertir la cadena de texto JSON a un objeto JSON

        # Extraer la información necesaria del objeto JSON
        transacciones = event_data["transacciones"]
        llave_publica = event_data["llave_publica"]
        firma_digital = event_data["firma_digital"]

        if transacciones:
            print("transacciones OK")
        if llave_publica:
            print("llave OK")
        if firma_digital:
            print("firma OK")
        # Convertir transacciones a JSON y luego a bytes
        transactions_json = json_lib.dumps(transacciones, separators=(",", ":")).encode(
            "utf-8"
        )
        print(f"Transacciones JSON (bytes):\n{transactions_json}")

        # Cargar la clave pública desde el PEM
        public_key_pem = llave_publica.encode()
        print(f"Public Key PEM:\n{public_key_pem.decode()}")

        public_key = serialization.load_pem_public_key(public_key_pem)

        # Convertir la firma digital de hex a bytes
        firma_digital_bytes = bytes.fromhex(firma_digital)
        print(f"Firma Digital (hex):\n{firma_digital}")
        print(f"Firma Digital (bytes):\n{firma_digital_bytes}")

        # Verificar la firma
        public_key.verify(
            firma_digital_bytes,
            transactions_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        print("La firma digital es válida")
        return True

    except Exception as e:
        print(f"Error verificando la firma digital: {str(e)}")
        return False


def encrypt_transactions(transactions: list) -> bytes:
    return transactions
    transactions_json = json_lib.dumps(transactions).encode("utf-8")

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(transactions_json) + padder.finalize()

    # Generar una nueva clave y IV para cada transacción
    key = b"This is a key123This is a key123"
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return iv + encrypted_data


def decrypt_transactions(encrypted_data: bytes) -> list:
    key = b"This is a key123This is a key123"
    iv = encrypted_data[:16]
    encrypted_transactions = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = (
        decryptor.update(encrypted_transactions) + decryptor.finalize()
    )

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    transactions = json_lib.loads(decrypted_data.decode("utf-8"))
    return transactions
