from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from ..database import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime
import uuid
import os
import requests

router = APIRouter()

def get_animals():
    response = requests.get("http://localhost:8003/animals/animals")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Erro ao buscar dados dos animais")

@router.get("/animals", response_model=list)
def fetch_animals():
    return get_animals()

@router.post("/sightings")
async def create_sighting(
    animal_id: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    date_time: datetime = Form(...),
    photo: UploadFile = File(None)
):
    photo_url = None
    if photo:
        photo_filename = f"{uuid.uuid4()}.jpg"
        photo_path = os.path.join("static", "photos", photo_filename)
        with open(photo_path, "wb") as f:
            f.write(await photo.read())
        photo_url = f"/static/photos/{photo_filename}"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sightings (animal_id, latitude, longitude, date_time, photo_url)
        VALUES (%s, %s, %s, %s, %s)
    """, (animal_id, latitude, longitude, date_time, photo_url))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Sighting registered successfully"}
