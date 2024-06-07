from fastapi import FastAPI
from animals_service.server.routers.animals import router as animals_router

# Instância do FastAPI para o microsserviço de animais
app = FastAPI()

# Inclui o router de animais, que contém os endpoints relacionados aos microsserviço animals_service.
app.include_router(animals_router, tags=["animals"], prefix="/animals")
