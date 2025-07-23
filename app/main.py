from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import create_db_and_tables
from app.routes import auth, leyendas, public
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI(
    title="4thewords API",
    description="API para gestionar leyendas costarricenses",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount(
    "/static",
    StaticFiles(directory=os.path.join("app", "static")),
    name="static"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Rutas
app.include_router(public.router)
app.include_router(auth.router)
app.include_router(leyendas.router)

