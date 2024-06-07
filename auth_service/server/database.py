import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Função para obter uma conexão com o banco de dados PostgreSQL.

    Returns:
        Retorna a conexão.
    """
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        database="auth",
        password="admin",
        port=5432
    )
    return conn

def create_tables():
    """
    Função para criar tabelas no banco de dados.

    Cria a tabela 'users' se ela não existir. Esta tabela armazena informações de usuários para fins de autenticação.

    Returns:
        None
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hash_password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Chamada da função para criar tabelas ao executar este script
create_tables()
