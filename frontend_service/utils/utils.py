from datetime import datetime, timedelta
from typing import Optional
import jwt

SECRET_KEY = "jellyfish"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Função para criar um token de acesso JWT.

    Args:
        data (dict): Os dados a serem codificados no token.
        expires_delta (Optional[timedelta]): O tempo de expiração do token. Padrão é 15 minutos.

    Returns:
        str: O token de acesso JWT codificado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Função para verificar a validade de um token de acesso JWT.

    Args:
        token (str): O token JWT a ser verificado.

    Returns:
        Union[dict, None]: O payload do token se for válido, caso contrário, None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
