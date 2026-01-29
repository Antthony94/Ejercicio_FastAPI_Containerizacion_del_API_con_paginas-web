import os
from sqlmodel import create_engine, SQLModel, Session
from src.models.videojuego import Videojuego
from datetime import date


db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_server = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 3306))
db_name = os.getenv("DB_NAME", "videojuegos_db")


if db_port == 5432:
    
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    print(" MODO: PostgreSQL detectado.")
else:
    
    DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    print(" MODO: MySQL detectado.")

print(f" Conectando a: {db_server}:{db_port}...")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        
        if not session.query(Videojuego).first():
            print(" Insertando la colección de Steam...")
            
            mis_juegos = [
                Videojuego(titulo="Black Myth: Wukong", es_multijugador=False, fecha_lanzamiento=date(2024, 8, 20)),
                Videojuego(titulo="Baldur's Gate 3", es_multijugador=True, fecha_lanzamiento=date(2023, 8, 3)),
                Videojuego(titulo="Cyberpunk 2077", es_multijugador=False, fecha_lanzamiento=date(2020, 12, 10)),
                Videojuego(titulo="Counter-Strike 2", es_multijugador=True, fecha_lanzamiento=date(2023, 9, 27)),
                Videojuego(titulo="Hogwarts Legacy", es_multijugador=False, fecha_lanzamiento=date(2023, 2, 10)),
                Videojuego(titulo="Rust", es_multijugador=True, fecha_lanzamiento=date(2018, 2, 8)),
                Videojuego(titulo="Blasphemous 2", es_multijugador=False, fecha_lanzamiento=date(2023, 8, 24)),
                Videojuego(titulo="It Takes Two", es_multijugador=True, fecha_lanzamiento=date(2021, 3, 26))
            ]

            session.add_all(mis_juegos)
            session.commit()
            print(" ¡Esta es mi coleccion real de videojuegos en STEAM!")