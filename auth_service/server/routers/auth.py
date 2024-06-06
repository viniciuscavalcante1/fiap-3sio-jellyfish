from datetime import timedelta

from fastapi import APIRouter, Request, status, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
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

@router.get("/login")
def login_get(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)

@router.post("/login")
def login_post(request: Request, email: str = Form(...), senha: str = Form(...)):
    usuario_autenticado, email_usuario = autenticar_usuario(email, senha)
    # TODO: alterar response
    if usuario_autenticado:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email_usuario}, expires_delta=access_token_expires
        )
        response = RedirectResponse(url=f"/auth/index", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
    else:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/register")
def register_get(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('register.html', context)

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
    response = RedirectResponse(url=f"/auth/login", status_code=status.HTTP_302_FOUND)
    return response

@router.get("/index")
def dashboard(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")
    payload = verify_token(token.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Não autorizado")
    email_usuario = payload.get("sub")
    context = {'request': request, 'email': email_usuario}
    return {"Eita, deu certo!"}
