import fastapi as _fastapi
import fastapi.middleware.cors as _CORS
import fastapi.staticfiles as _staticfiles

from routers.user_router import router as user_router
from routers.token_router import router as token_router
from routers.event_router import router as event_router
from routers.event_user_router import router as eu_router
from routers.util_router import router as util_router

app = _fastapi.FastAPI()
origins = [
    "http://localhost:5173",
    "http://192.168.1.18:5173",
    "https://cbcb-179-57-154-53.ngrok-free.app",
    "https://d727-179-57-154-53.ngrok-free.app",
]

app.add_middleware(
    _CORS.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/data", _staticfiles.StaticFiles(directory="data"), name="data")

app.include_router(user_router)
app.include_router(token_router)
app.include_router(event_router)
app.include_router(eu_router)
app.include_router(util_router)
