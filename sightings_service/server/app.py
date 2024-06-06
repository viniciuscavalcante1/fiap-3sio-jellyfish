from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sightings_service.server.routers.sightings import router as sightings_router
from pathlib import Path
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.include_router(sightings_router, tags=["sightings"], prefix="/sightings")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
