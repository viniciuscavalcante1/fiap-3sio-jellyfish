from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rescue_service.server.routers.rescue import router as rescue_router

app = FastAPI()

origins = [
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rescue_router, prefix="/rescue", tags=["rescue"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
