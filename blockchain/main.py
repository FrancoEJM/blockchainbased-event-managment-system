import os
import signal
import logging
import fastapi as _fastapi
import fastapi.middleware.cors as _CORS

from dotenv import load_dotenv
from services import (
    database_services as db_sv,
    sync_services as sync_sv,
)
from init.init_router import router as init_router
from routers.status_router import router as status_router
from routers.blockchain_router import router as blc_router
from routers.consensus_router import router as poet_router
from routers.transactions_router import router as tx_router
from routers.block_router import router as block_router
from routers.node_router import router as node_router
from main3 import router as test_router

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener IP y puerto desde las variables de entorno
IP = os.getenv("IP", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DATABASE_URL = os.getenv("DATABASE_URL")
NODE_ID = int(os.getenv("NODE_ID"))

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

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
app.include_router(poet_router)
app.include_router(tx_router)
app.include_router(test_router)
app.include_router(block_router)
app.include_router(node_router)


@app.on_event("startup")
async def startup_event():
    db_gen = db_sv.get_db()
    db = next(db_gen)
    logging.info("Inicializando nodo...")
    logging.info("------------------------------------------------------")
    await sync_sv.update_and_notify_status(IP, PORT, True, NODE_ID, db)
    logging.info("------------------------------------------------------")


@app.on_event("shutdown")
async def shutdown_event():
    db_gen = db_sv.get_db()
    db = next(db_gen)
    logging.info("Finalizando nodo...")
    logging.info("------------------------------------------------------")
    await sync_sv.update_and_notify_status(IP, PORT, False, NODE_ID, db)
    logging.info("------------------------------------------------------")


# Endpoint para apagar el servidor
@app.get("/shutdown")
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return _fastapi.Response(status_code=200, content="Server shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=IP, port=PORT)
