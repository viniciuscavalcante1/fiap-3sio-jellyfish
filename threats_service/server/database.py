import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Objeto de conexão com o banco de dados.
    """
    conn = psycopg2.connect(
        host="localhost",
        database="threats",
        user="postgres",
        password="admin"
    )
    return conn

def create_tables():
    """
    Cria a tabela 'threat_reports' no banco de dados se ela não existir.

    Raises:
        psycopg2.Error: Se ocorrer algum erro ao executar a consulta SQL.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
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
    except psycopg2.Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

create_tables()
