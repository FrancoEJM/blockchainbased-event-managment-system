import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(destinatario, asunto, cuerpo, es_html=False, archivo_adjunto=None):
    servidor = os.getenv('SMTP_SERVER')
    puerto = os.getenv('SMTP_PORT')
    usuario = os.getenv('EMAIL_USER')
    contraseña = os.getenv('EMAIL_PASSWORD')

    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    if es_html:
        mensaje.attach(MIMEText(cuerpo, 'html'))
    else:
        mensaje.attach(MIMEText(cuerpo, 'plain'))

    if archivo_adjunto:
        # Adjunta el archivo
        adjunto = MIMEBase('application', 'octet-stream')
        adjunto.set_payload(open(archivo_adjunto, 'rb').read())
        encoders.encode_base64(adjunto)
        adjunto.add_header('Content-Disposition', f'attachment; filename={os.path.basename(archivo_adjunto)}')
        mensaje.attach(adjunto)

    # Conecta al servidor SMTP
    servidor_smtp = smtplib.SMTP(servidor, puerto)
    servidor_smtp.starttls()
    servidor_smtp.login(usuario, contraseña)

    # Envía el correo
    texto = mensaje.as_string()
    servidor_smtp.sendmail(usuario, destinatario, texto)
    servidor_smtp.quit()
