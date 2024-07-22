from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json as json_lib

app = FastAPI()



@app.post("/verify")
async def verify_event_data(event_data: str):
    try:
        # Convertir la cadena de texto JSON a un objeto JSON
        event_data_json = json_lib.loads(event_data)

        # Extraer la información necesaria del objeto JSON
        transacciones = event_data_json["transacciones"]
        llave_publica = event_data_json["llave_publica"]
        firma_digital = event_data_json["firma_digital"]

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
        return {"status": "success", "message": "La firma digital es válida"}

    except Exception as e:
        print(f"Error verificando la firma digital: {str(e)}")
        raise HTTPException(
            status_code=400, detail=f"La firma digital no es válida: {str(e)}"
        )


# Levantar la aplicación en el puerto 8001
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
