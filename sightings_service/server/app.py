from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sightings_service.server.routers.sightings import router as sightings_router
from pathlib import Path
from fastapi.templating import Jinja2Templates

# Inicializa os templates Jinja
templates = Jinja2Templates(directory='templates')

# Cria uma instância do FastAPI
app = FastAPI()

# Permite redirects para o microsserviço de frontend
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

# Inclui o router de avistamentos
app.include_router(sightings_router, tags=["sightings"], prefix="/sightings")

# Monta o diretório de arquivos estáticos
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),  # Caminho para o diretório de arquivos estáticos
    name="static",
)
