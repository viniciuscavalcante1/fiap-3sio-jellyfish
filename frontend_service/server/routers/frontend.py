from fastapi import APIRouter, Request, status, Form, HTTPException, Depends
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from requests import post, get

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


@router.get("/register_sighting")
def register_sighting_get(request: Request):
    print("Teste")
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        print("not token")
        raise HTTPException(status_code=401, detail="Não autorizado")
    payload = verify_token(token.split(" ")[1])
    print("payload:")
    print(payload)
    if not payload:
        print("not payload :(")
        raise HTTPException(status_code=401, detail="Não autorizado")

    user_id = payload.get("sub")
    animals_response = get("http://localhost:8003/animals/animals")
    if animals_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao buscar dados dos animais")

    animals = animals_response.json()

    context = {
        'request': request,
        'user_id': user_id,
        'animals': animals
    }
    return templates.TemplateResponse('register_sighting.html', context)


@router.get("/report_threat")
def register_sighting(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")
    payload = verify_token(token.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Não autorizado")
    email_usuario = payload.get("sub")
    context = {'request': request, 'email': email_usuario}
    return templates.TemplateResponse('report_threat.html', context)


@router.get("/request_rescue")
def register_sighting(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")
    payload = verify_token(token.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Não autorizado")
    email_usuario = payload.get("sub")
    context = {'request': request, 'email': email_usuario}
    return templates.TemplateResponse('request_rescue.html', context)


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


@router.get("/export")
async def get_export_data(request: Request):
    return templates.TemplateResponse("export.html", {"request": request})


@router.get("/learn")
async def get_education(request: Request):
    articles = [
        {
            "title": "Como identificar os seres marinhos",
            "description": "Aprenda a identificar diferentes espécies marinhas.",
            "link": "https://www.oceanopedia.com.br/l/como-identificar-os-seres-marinhos/"
        },
        {
            "title": "Procedimentos de resgate de animais marinhos",
            "description": "Saiba o que fazer quando encontrar animais marinhos encalhados ou machucados.",
            "link": "https://iema.es.gov.br/Not%C3%ADcia/saiba-o-que-fazer-quando-encontrar-animais-marinhos-encalhados-ou-machucados"
        },
        {
            "title": "Espécies marinhas em risco de extinção",
            "description": "Conheça 5 animais marinhos ameaçados de extinção.",
            "link": "https://www.nationalgeographicbrasil.com/animais/2023/06/conheca-5-animais-marinhos-ameacados-de-extincao"
        },
        {
            "title": "Como reduzir a poluição nos oceanos",
            "description": "4 formas de colaborar com o fim da poluição nos oceanos.",
            "link": "https://umsoplaneta.globo.com/patrocinado/natura/noticia/2022/01/13/4-formas-de-colaborar-com-o-fim-da-poluicao-nos-oceanos.ghtml"
        }
    ]
    return templates.TemplateResponse("learn.html", {"request": request, "articles": articles})


@router.get("/support")
async def get_support(request: Request):
    organizations = [
        {
            "name": "A Voz dos Oceanos",
            "description": "A Voz dos Oceanos é um movimento mundial de combate à poluição plástica.",
            "link": "https://voiceoftheoceans.com/"
        },
        {
            "name": "Sea Shepherd",
            "description": "A Sea Shepherd defende, conserva e protege a vida e os habitats marinhos.",
            "link": "https://seashepherd.org.br/"
        },
        {
            "name": "Instituto Gremar",
            "description": "O Instituto Gremar é uma organização focada no resgate de animais marinhos.",
            "link": "https://gremar.org.br/"
        },
        {
            "name": "Fundação Mamíferos Aquáticos",
            "description": "A Fundação Mamíferos Aquáticos trabalha conservar os mamíferos aquáticos e seus habitats.",
            "link": "https://mamiferosaquaticos.org.br/"
        },
    ]
    return templates.TemplateResponse("support.html", {"request": request, "organizations": organizations})


@router.get("/success")
async def get_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})