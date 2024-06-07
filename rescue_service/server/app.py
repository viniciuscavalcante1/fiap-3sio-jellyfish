from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rescue_service.server.routers.rescue import router as rescue_router

# Cria uma instância da FastAPI
app = FastAPI()

# Permite redirect pra rota do frontend_service
origins = [
    "http://localhost:8001",
]

# Adiciona o middleware CORSMiddleware para permitir requisições CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router de resgate com os endpoints do microsserviço rescue_service
app.include_router(rescue_router, prefix="/rescue", tags=["rescue"])

# Inicia o servidor somente se este script for executado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
