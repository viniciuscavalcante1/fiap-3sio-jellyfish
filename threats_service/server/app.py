from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threats_service.server.routers.threats import router as threats_router

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

app.include_router(threats_router, prefix="/threat_reports", tags=["threat_reports"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
