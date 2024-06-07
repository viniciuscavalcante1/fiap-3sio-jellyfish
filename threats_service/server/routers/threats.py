from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from ..database import get_db_connection
from datetime import datetime
import uuid
import os
import requests

# Cria o router
router = APIRouter()

# URL do serviço de autenticação
AUTH_SERVICE_URL = "http://localhost:8000"


def get_user_id_by_email(email: str):
    """
    Obtém o ID do usuário com base no endereço de e-mail.

    Args:
        email (str): Endereço de e-mail do usuário.

    Returns:
        int: ID do usuário.

    Raises:
        HTTPException: Se não for possível encontrar o usuário.
    """
    response = requests.post(f"{AUTH_SERVICE_URL}/auth/get_user_id", data={"email": email})
    if response.status_code == 200:
        return response.json()["user_id"]
    else:
        raise HTTPException(status_code=response.status_code, detail="User not found")


@router.post("/create")
async def create_threat_report(
        threat_type: str = Form(...),
        latitude: float = Form(...),
        longitude: float = Form(...),
        date_time: datetime = Form(...),
        description: str = Form(...),
        photo: UploadFile = File(None),
        user_email: str = Form(...)
):
    """
    Cria um novo relatório de ameaça.

    Args:
        threat_type (str): Tipo de ameaça.
        latitude (float): Latitude da localização da ameaça.
        longitude (float): Longitude da localização da ameaça.
        date_time (datetime): Data e hora do relatório.
        description (str): Descrição da ameaça.
        photo (UploadFile, optional): Foto da ameaça (se disponível). Defaults to None.
        user_email (str): E-mail do usuário que cria o relatório.

    Returns:
        dict: Mensagem indicando que o relatório de ameaça foi criado com sucesso.
    """
    # Obtém o ID do usuário com base no e-mail fornecido
    user_id = get_user_id_by_email(user_email)

    # Verifica se uma foto foi fornecida e salva-a no diretório correspondente
    photo_url = None
    if photo:
        photo_directory = "static/threat_photos"
        os.makedirs(photo_directory, exist_ok=True)
        photo_filename = f"{uuid.uuid4()}.jpg"
        photo_path = os.path.join(photo_directory, photo_filename)
        with open(photo_path, "wb") as f:
            f.write(await photo.read())
        photo_url = f"/static/threat_photos/{photo_filename}"

    # Insere os dados do relatório de ameaça no banco de dados
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO threat_reports (threat_type, latitude, longitude, date_time, description, photo_url, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (threat_type, latitude, longitude, date_time, description, photo_url, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Threat report created successfully"}


@router.get("/")
async def get_threat_reports():
    """
    Obtém todos os relatórios de ameaça do banco de dados.

    Returns:
        list: Lista de relatórios de ameaça.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM threat_reports")
    reports = cur.fetchall()
    cur.close()
    conn.close()
    return reports


@router.get("/export")
async def export_threat_reports():
    """
    Exporta todos os relatórios de ameaça do banco de dados.

    Returns:
        list: Lista de relatórios de ameaça.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM threat_reports")
    threats = cur.fetchall()
    cur.close()
    conn.close()
    return threats
