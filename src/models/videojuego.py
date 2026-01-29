from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date



class Videojuego(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    es_multijugador: bool
    fecha_lanzamiento: Optional[date] = None