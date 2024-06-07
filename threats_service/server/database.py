import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="threats",
        user="postgres",
        password="admin"
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS threat_reports (
        id SERIAL PRIMARY KEY,
        threat_type VARCHAR(255) NOT NULL,
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


create_tables()
