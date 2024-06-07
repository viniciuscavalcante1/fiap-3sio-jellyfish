import uvicorn
if __name__ == "__main__":
    # Inicia microsserviço rescue_service
    uvicorn.run("server.app:app", host="0.0.0.0", port=8004, reload=True)
