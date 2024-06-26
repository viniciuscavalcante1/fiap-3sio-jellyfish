from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from ..database import get_db_connection
from datetime import datetime
import uuid
import os
import requests

router = APIRouter()

AUTH_SERVICE_URL = "http://localhost:8000"

def get_user_id_by_email(email: str):
    response = requests.post(f"{AUTH_SERVICE_URL}/auth/get_user_id", data={"email": email})
    if response.status_code == 200:
        return response.json()["user_id"]
    else:
        raise HTTPException(status_code=response.status_code, detail="User not found")

@router.post("/create")
async def create_rescue_request(
    animal_type: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    date_time: datetime = Form(...),
    description: str = Form(...),
    photo: UploadFile = File(None),
    user_email: str = Form(...)
):
    user_id = get_user_id_by_email(user_email)

    photo_url = None
    if photo:
        photo_directory = "static/rescue_photos"
        os.makedirs(photo_directory, exist_ok=True)
        photo_filename = f"{uuid.uuid4()}.jpg"
        photo_path = os.path.join(photo_directory, photo_filename)
        with open(photo_path, "wb") as f:
            f.write(await photo.read())
        photo_url = f"/static/rescue_photos/{photo_filename}"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO rescue_requests (animal_type, latitude, longitude, date_time, description, photo_url, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (animal_type, latitude, longitude, date_time, description, photo_url, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Rescue request created successfully"}

@router.get("/")
async def get_rescue_requests():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rescue_requests")
    requests = cur.fetchall()
    cur.close()
    conn.close()
    return requests


@router.get("/export")
async def export_rescue_requests():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM rescue_requests")
    rescues = cur.fetchall()
    cur.close()
    conn.close()
    return rescues
