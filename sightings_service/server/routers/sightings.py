from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from ..database import get_db_connection
from datetime import datetime
import uuid
import os
import requests

# Cria router
router = APIRouter()

# URL do serviço de autenticação
AUTH_SERVICE_URL = "http://localhost:8000"


def get_user_id_by_email(email: str):
    """
    Função para obter o ID de usuário usando o serviço de autenticação.

    Args:
        email (str): O endereço de e-mail do usuário.

    Returns:
        int: O ID de usuário.

    Raises:
        HTTPException: Se o serviço de autenticação retornar um código de status de erro.
    """
    response = requests.post(f"{AUTH_SERVICE_URL}/auth/get_user_id", data={"email": email})
    if response.status_code == 200:
        return response.json()["user_id"]
    else:
        raise HTTPException(status_code=response.status_code, detail="User not found")


@router.post("/sightings")
async def create_sighting(
        animal_id: int = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        date_time: datetime = Form(...),
        photo: UploadFile = File(None),
        user_email: str = Form(...)
):
    """
    Rota para criar um novo avistamento.

    Args:
        animal_id (int): O ID do animal avistado.
        latitude (float): A latitude do local do avistamento.
        longitude (float): A longitude do local do avistamento.
        date_time (datetime): A data e hora do avistamento.
        photo (UploadFile): O arquivo de foto do avistamento (opcional).
        user_email (str): O endereço de e-mail do usuário que fez o avistamento.

    Returns:
        dict: Uma mensagem indicando que o avistamento foi registrado com sucesso.
    """
    # Obtém o ID de usuário usando o endereço de e-mail
    user_id = get_user_id_by_email(user_email)

    # Salva a foto do avistamento e obtém sua URL, se fornecida
    photo_url = None
    if photo:
        photo_directory = "static/photos"
        os.makedirs(photo_directory, exist_ok=True)
        photo_filename = f"{uuid.uuid4()}.jpg"
        photo_path = os.path.join(photo_directory, photo_filename)
        with open(photo_path, "wb") as f:
            f.write(await photo.read())
        photo_url = f"/static/photos/{photo_filename}"

    # Conecta-se ao banco de dados e insere os dados do avistamento
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sightings (animal_id, latitude, longitude, date_time, photo_url, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (animal_id, latitude, longitude, date_time, photo_url, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Sighting registered successfully"}


@router.get("/export")
async def export_sightings():
    """
    Rota para exportar todos os avistamentos registrados no banco de dados.

    Returns:
        list: Uma lista de dicionários contendo os dados de todos os avistamentos.
    """
    # Conecta-se ao banco de dados e recupera todos os avistamentos
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sightings")
    sightings = cur.fetchall()
    cur.close()
    conn.close()
    return sightings
