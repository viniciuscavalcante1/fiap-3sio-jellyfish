from fastapi import APIRouter, Request, status, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from ..database import get_db_connection
from psycopg2.extras import RealDictCursor
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory='templates')

usuario_autenticado = False
email_usuario = None

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
    global usuario_autenticado, email_usuario
    usuario_autenticado, email_usuario = autenticar_usuario(email, senha)
    # TODO: alterar response
    if usuario_autenticado:
        response = RedirectResponse(url=f"/index", status_code=status.HTTP_302_FOUND)
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

@router.get("/dashboard")
def dashboard(request: Request):
    if not usuario_autenticado:
        raise HTTPException(status_code=401, detail="Não autorizado")
    context = {'request': request, 'email': email_usuario}
    return templates.TemplateResponse('dashboard.html', context)
