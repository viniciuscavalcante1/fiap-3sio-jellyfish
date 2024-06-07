from fastapi import FastAPI
from auth_service.server.routers.auth import router as auth_router

app = FastAPI()

# Inclui router do microsserviço auth_service
app.include_router(auth_router, tags=["auth"], prefix="/auth")
