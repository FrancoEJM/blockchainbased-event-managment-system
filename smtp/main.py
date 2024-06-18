from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from send_email import enviar_correo

app = FastAPI()


class Correo(BaseModel):
    destinatario: str
    asunto: str
    cuerpo: str
    es_html: bool = True
    ruta_imagen: str


@app.post("/enviar-correo/")
def enviar_correo_endpoint(correo: Correo):
    try:
        print(
            f"correo.destinatario: {correo.destinatario}",
            f"correo.asunto: {correo.asunto}",
            f"correo.cuerpo: {correo.cuerpo}",
            f"correo.es_html: {correo.es_html}",
            f"correo.ruta_imagen: {correo.ruta_imagen}",
        )

        enviar_correo(
            correo.destinatario,
            correo.asunto,
            correo.cuerpo,
            correo.es_html,
            correo.ruta_imagen,
        )
        return {"correo": "Correo enviado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
