from fastapi import APIRouter, Request, status, Form, HTTPException, Depends
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from requests import post

SECRET_KEY = "jellyfish"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
templates = Jinja2Templates(directory='templates')


def verify_token(token: str):
    response = post("http://localhost:8000/auth/verify_token", data={"token": token})
    if response.status_code == 200:
        return response.json()
    else:
        return None

@router.get("/dashboard")
def dashboard(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")
    payload = verify_token(token.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Não autorizado")
    email_usuario = payload.get("sub")
    context = {'request': request, 'email': email_usuario}
    return templates.TemplateResponse('dashboard.html', context)


@router.get("/login")
def login_get(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)


@router.post("/login")
def login_post(request: Request, email: str = Form(...), senha: str = Form(...)):
    response = post("http://localhost:8000/auth/login", data={"email": email, "senha": senha})
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
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
    response = post("http://localhost:8000/auth/register", data={"email": email, "senha": senha})
    if response.status_code == 200:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    else:
        raise HTTPException(status_code=400, detail="Erro ao registrar usuário")