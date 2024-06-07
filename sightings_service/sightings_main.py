import uvicorn
if __name__ == "__main__":
    # Inicia o microsserviço sightings_service
    uvicorn.run("server.app:app", host="0.0.0.0", port=8002, reload=True)
