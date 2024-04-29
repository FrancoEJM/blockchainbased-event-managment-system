import fastapi as _fastapi
import fastapi.security as _security
import fastapi.middleware.cors as _CORS

import sqlalchemy.orm as _orm

from routers.user_router import router as user_router
from routers.token_router import router as token_router
from routers.event_router import router as event_router

from typing import List

app = _fastapi.FastAPI()
origins = [
   "http://localhost:5173" 
]

app.add_middleware(
    _CORS.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(token_router)
app.include_router(event_router)