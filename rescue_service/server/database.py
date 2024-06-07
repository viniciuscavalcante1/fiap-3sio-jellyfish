import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """
    Função para estabelecer uma conexão com o banco de dados do microsserviço rescue_service.

    Returns:
        psycopg2.extensions.connection: Uma conexão com o banco de dados PostgreSQL.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="rescue",
        user="postgres",
        password="admin"
    )
    return conn


def create_tables():
    """
    Função para criar a tabela "rescue_requests" no banco de dados, se ainda não existir.

    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rescue_requests (
            id SERIAL PRIMARY KEY,
            animal_type VARCHAR(255) NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            date_time TIMESTAMP NOT NULL,
            description TEXT NOT NULL,
            photo_url VARCHAR(255),
            user_id INTEGER NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# Chama a função create_tables para criar a tabela "rescue_requests" se ainda não existir
create_tables()
