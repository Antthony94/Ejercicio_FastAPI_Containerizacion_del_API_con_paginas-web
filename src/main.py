import time
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from src.data.db import init_db, get_session, Session
from src.models.videojuego import Videojuego


templates = Jinja2Templates(directory="src/templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" DOCKER: Arrancando la aplicación...")
    for _ in range(10):
        try:
            init_db()
            print(" DOCKER: Base de datos conectada.")
            break
        except Exception as e:
            print(" Esperando a la Base de Datos...")
            time.sleep(2)
    yield
    print(" Apagando...")

app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def ver_pagina_juegos(request: Request, session: Session = Depends(get_session)):
    try:
        juegos = session.exec(select(Videojuego)).all()
        return templates.TemplateResponse("lista_juegos.html", {"request": request, "juegos": juegos})
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"


@app.get("/juego/{juego_id}", response_class=HTMLResponse)
def ver_detalle_juego(juego_id: int, request: Request, session: Session = Depends(get_session)):
    juego = session.get(Videojuego, juego_id)
    if not juego:
        return "<h1>Juego no encontrado</h1>"
    return templates.TemplateResponse("detalle_juego.html", {"request": request, "juego": juego})


@app.post("/juego/{juego_id}")
async def actualizar_juego(
    juego_id: int,
    titulo: str = Form(...),
    fecha_lanzamiento: str = Form(...),
    es_multijugador: bool = Form(False),
    session: Session = Depends(get_session)
):
    juego = session.get(Videojuego, juego_id)
    if juego:
        juego.titulo = titulo
        juego.fecha_lanzamiento = datetime.strptime(fecha_lanzamiento, '%Y-%m-%d').date()
        juego.es_multijugador = es_multijugador
        session.add(juego)
        session.commit()
    
    return RedirectResponse(url="/", status_code=303)


@app.get("/nuevo", response_class=HTMLResponse)
def formulario_nuevo_juego(request: Request):
    return templates.TemplateResponse("crear_juego.html", {"request": request})


@app.post("/crear")
async def crear_juego_nuevo(
    titulo: str = Form(...),
    fecha_lanzamiento: str = Form(...),
    es_multijugador: bool = Form(False),
    session: Session = Depends(get_session)
):
    
    nuevo_juego = Videojuego(
        titulo=titulo,
        fecha_lanzamiento=datetime.strptime(fecha_lanzamiento, '%Y-%m-%d').date(),
        es_multijugador=es_multijugador
    )
    
    
    session.add(nuevo_juego)
    session.commit()
    
    return RedirectResponse(url="/", status_code=303)