import uvicorn
if __name__ == "__main__":
    # Inicia o microsserviço threats_service
    uvicorn.run("server.app:app", host="0.0.0.0", port=8005, reload=True)
