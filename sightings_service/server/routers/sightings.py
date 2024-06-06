from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends, Header
from ..database import get_db_connection
from datetime import datetime
import uuid
import os
import requests

router = APIRouter()

def verify_token(token: str):
    response = requests.post("http://localhost:8000/auth/verify_token", data={"token": token})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=401, detail="Não autorizado.")

@router.post("/sightings")
async def create_sighting(
    animal_id: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    date_time: datetime = Form(...),
    photo: UploadFile = File(None),
    authorization: str = Header(...)
):
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    user_id = payload.get("sub")

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
        INSERT INTO sightings (animal_id, latitude, longitude, date_time, photo_url, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (animal_id, latitude, longitude, date_time, photo_url, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Sighting registered successfully"}
