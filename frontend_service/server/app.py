from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from frontend_service.server.routers.frontend import router as frontend_router
from pathlib import Path
from fastapi.templating import Jinja2Templates

# Inicia diretório Jinja para renderizar templates HTML
templates = Jinja2Templates(directory='templates')

# Inicializa app FastAPI
app = FastAPI()

# Inclui router do microsserviço frontend_service
app.include_router(frontend_router, tags=["dashboard"], prefix="")

# Adiciona a pasta static
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
