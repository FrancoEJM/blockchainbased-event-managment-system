import os
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import fastapi.middleware.cors as _CORS
from dotenv import load_dotenv
from models.blc_models import NODOS
from contextlib import asynccontextmanager
from services import database_services as db_sv
from init.init_router import router as init_router
from routers.status_router import router as status_router
from routers.blockchain_router import router as blc_router

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener IP y puerto desde las variables de entorno
IP = os.getenv("IP", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DATABASE_URL = os.getenv("DATABASE_URL")


# @asynccontextmanager
# async def lifespan(app: _fastapi.FastAPI):
#     # Aquí debes crear una sesión de base de datos
#     db = db_sv.get_db()  # Asegúrate de que esta función devuelva una sesión válida
#     try:
#         # Filtrar por IP y puerto
#         nodo = db.query(NODOS).filter(NODOS.ip == IP, NODOS.port == PORT).first()

#         # Cambiar el status a True si se encuentra el nodo
#         if nodo:
#             nodo.status = True
#             db.commit()
#             db.refresh(nodo)
#             print("Se ha encendido el nodo.")

#         yield  # Aquí se pausa y se espera a que la aplicación reciba solicitudes

#     finally:
#         db.close()  # Cierra la sesión de base de datos al terminar


# app = _fastapi.FastAPI(lifespan=lifespan)
app = _fastapi.FastAPI()
origins = ["http://localhost:8000", "http://localhost:8001"]

app.add_middleware(
    _CORS.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blc_router)
app.include_router(status_router)
app.include_router(init_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=IP, port=PORT)
