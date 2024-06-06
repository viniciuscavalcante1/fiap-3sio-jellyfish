from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from animals_service.server.routers.auth import router as animals_router
from pathlib import Path
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.include_router(animals_router, tags=["auth"], prefix="/auth")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
