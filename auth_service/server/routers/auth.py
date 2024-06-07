from datetime import timedelta, datetime

from fastapi import APIRouter, Request, status, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.templating import Jinja2Templates
from ..database import get_db_connection
from ...utils.utils import create_access_token, verify_token
from psycopg2.extras import RealDictCursor
import hashlib

SECRET_KEY = "jellyfish"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
templates = Jinja2Templates(directory='templates')


def autenticar_usuario(email, senha):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    usuario_encontrado = cur.fetchone()
    cur.close()
    conn.close()
    if usuario_encontrado is not None:
        senha_hash = hashlib.md5(senha.encode()).hexdigest()
        if senha_hash == usuario_encontrado['hash_password']:
            return True, email
        else:
            return False, "SENHA INCORRETA"
    else:
        return False, "USUARIO NAO ENCONTRADO"


@router.post("/login")
def login_post(request: Request, email: str = Form(...), senha: str = Form(...)):
    usuario_autenticado, email_usuario = autenticar_usuario(email, senha)
    if usuario_autenticado:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email_usuario}, expires_delta=access_token_expires
        )
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60)
        return response
    else:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/register")
def register_post(request: Request, email: str = Form(...), senha: str = Form(...)):
    hash_password = hashlib.md5(senha.encode()).hexdigest()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (email, hash_password) VALUES (%s, %s)", (email, hash_password))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Erro ao registrar usuário.")
    cur.close()
    conn.close()
    return JSONResponse(content={"message": "Usuário registrado com sucesso"})


@router.post("/verify_token")
def verify_token_endpoint(token: str = Form(...)):
    payload = verify_token(token)
    if payload:
        return JSONResponse(content=payload)
    else:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post("/get_user_id")
def get_user_id(email: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return {"user_id": user["id"]}
    else:
        raise HTTPException(status_code=404, detail="User not found")