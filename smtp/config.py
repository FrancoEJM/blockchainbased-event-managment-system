import uvicorn
import dotenv
import os

dotenv.load_dotenv()

BACKEND_SMTP_HOST = os.getenv('BACKEND_SMTP_HOST')
BACKEND_SMTP_PORT = os.getenv('BACKEND_SMTP_PORT')

if __name__ == "__main__":
    uvicorn.run("main:app", host=BACKEND_SMTP_HOST, port=int(BACKEND_SMTP_PORT), reload=True)
