import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Uma conexão com o banco de dados PostgreSQL.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="sightings",
        user="postgres",
        password="admin"
    )
    return conn


def create_tables():
    """
    Cria a tabela "sightings" no banco de dados, se ainda não existir.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sightings (
            id SERIAL PRIMARY KEY,
            animal_id INTEGER NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            date_time TIMESTAMP NOT NULL,
            photo_url TEXT,
            user_id INTEGER NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# Chama a função create_tables para criar a tabela "sightings" se ainda não existir
create_tables()
