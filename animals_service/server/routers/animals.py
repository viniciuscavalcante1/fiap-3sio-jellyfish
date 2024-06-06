from fastapi import APIRouter, UploadFile, File, Form
from ..database import get_db_connection
from ..models import Animal
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/animals", response_model=list[Animal])
def get_animals():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM animals")
    animals = cur.fetchall()
    cur.close()
    conn.close()
    return animals