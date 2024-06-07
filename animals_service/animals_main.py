import uvicorn
if __name__ == "__main__":
    # Roda o microsserviço animals_service
    uvicorn.run("server.app:app", host="0.0.0.0", port=8003, reload=True)