from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threats_service.server.routers.threats import router as threats_router

# Cria uma instância do FastAPI
app = FastAPI()

# Permite redirects para o frontend
origins = [
    "http://localhost:8001",
]

# Adiciona middleware para habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router de ameaças
app.include_router(threats_router, prefix="/threat_reports", tags=["threat_reports"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
