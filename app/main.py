from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db import create_db_and_tables
from app.routes import auth, leyendas

app = FastAPI(
    title="4thewords API",
    description="API para gestionar leyendas costarricenses",
    version="1.0.0"
)

# Habilitar CORS para permitir conexión con el frontend en el puerto 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas automáticamente al arrancar el servidor
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir rutas separadas por funcionalidad
app.include_router(auth.router)
app.include_router(leyendas.router)

