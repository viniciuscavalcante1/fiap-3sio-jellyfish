import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="animals",
        user="postgres",
        password="admin"
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            photo_url TEXT,
            description TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_initial_data():
    conn = get_db_connection()
    cur = conn.cursor()
    animals = [
        ("Tartaruga-marinha", "static/animal_photos/tartaruga_marinha.jpg", "Uma espécie de tartaruga encontrada em mares tropicais."),
        ("Golfinho", "static/animal_photos/golfinho.jpg", "Mamífero marinho conhecido por sua inteligência e brincadeiras."),
        ("Baleia", "static/animal_photos/baleia.jpg", "Os maiores mamíferos do planeta, encontrados em todos os oceanos."),
        ("Ouriço do Mar", "static/animal_photos/ourico_do_mar.jpg", "Animal marinho espinhoso encontrado em águas rasas."),
        ("Caravela", "static/animal_photos/caravela.jpg", "Colônia de organismos flutuantes conhecida por suas dolorosas picadas."),
        ("Água-viva", "static/animal_photos/agua_viva.jpg", "Animais marinhos com corpos gelatinosos e tentáculos. Além disso, é a origem do nome do nosso aplicativo! :)"),
        ("Bagre", "static/animal_photos/bagre.jpg", "Peixe de água doce e salgada."),
        ("Pinguim", "static/animal_photos/pinguim.jpg", "Ave marinha que não voa e vive em regiões frias."),
        ("Enguia-de-areia", "static/animal_photos/enguia_de_areia.jpg", "Enguia que se enterra na areia para se proteger."),
        ("Lobo marinho", "static/animal_photos/lobo_marinho.jpg", "Mamífero marinho encontrado em costas rochosas."),
        ("Leão-marinho", "static/animal_photos/leao_marinho.jpg", "Mamífero marinho com orelhas externas visíveis."),
        ("Gaivota", "static/animal_photos/gaivota.jpg", "Ave marinha comum em áreas costeiras."),
        ("Estrela-do-mar", "static/animal_photos/estrela_do_mar.jpg", "Invertebrado marinho com forma de estrela."),
        ("Caranguejo", "static/animal_photos/caranguejo.jpg", "Crustáceo com um corpo achatado e pinças."),
        ("Siri", "static/animal_photos/siri.jpg", "Crustáceo semelhante ao caranguejo, mas com um corpo mais estreito.")
    ]
    for animal in animals:
        cur.execute("INSERT INTO animals (name, photo_url, description) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING", animal)
    conn.commit()
    cur.close()
    conn.close()

create_tables()
insert_initial_data()
