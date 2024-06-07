from fastapi import APIRouter, UploadFile, File, Form
from ..database import get_db_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/animals")
def get_animals():
    """
    Rota para obter todos os animais, retorna uma lista de todos os animais no banco de dados.

    Returns:
        List[dict]: Uma lista de dicionários representando cada animal no banco de dados.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM animals")
    animals = cur.fetchall()
    cur.close()
    conn.close()
    return animals
