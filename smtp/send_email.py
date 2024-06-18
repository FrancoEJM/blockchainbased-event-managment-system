import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def enviar_correo(destinatario, asunto, cuerpo, es_html, ruta_imagen: str):
    servidor = os.getenv("SMTP_SERVER")
    puerto = os.getenv("SMTP_PORT")
    usuario = os.getenv("EMAIL_USER")
    contraseña = os.getenv("EMAIL_PASSWORD")

    mensaje = MIMEMultipart()
    mensaje["From"] = usuario
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    if es_html:
        mensaje.attach(MIMEText(cuerpo, "html"))
    else:
        mensaje.attach(MIMEText(cuerpo, "plain"))
    # ruta_imagen = "../backend/data/userPrivateQRImages/image.png"

    print("ruta_imagen", ruta_imagen)
    if ruta_imagen:
        with open(ruta_imagen, "rb") as img:
            imagen = MIMEImage(img.read())
            imagen.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(ruta_imagen)}"',
            )
            mensaje.attach(imagen)

    # Conecta al servidor SMTP
    servidor_smtp = smtplib.SMTP(servidor, puerto)
    servidor_smtp.starttls()
    servidor_smtp.login(usuario, contraseña)

    # Envía el correo
    texto = mensaje.as_string()
    servidor_smtp.sendmail(usuario, destinatario, texto)
    servidor_smtp.quit()
