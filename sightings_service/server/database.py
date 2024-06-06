import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        database="auth",
        password="admin",
        port=5432
    )
    return conn


def create_tables():
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


create_tables()
