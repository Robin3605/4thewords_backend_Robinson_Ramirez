# Leyendas  - API (Prueba Técnica 4thewords)

Este proyecto es una API REST construida con **FastAPI** y **MySQL**, desarrollada como parte de una prueba técnica. La API permite crear, listar, editar y eliminar leyendas con sus respectivas ubicaciones y categorías, autenticación mediante JWT, y manejo de imágenes.

---

## 🚀 Tecnologías utilizadas

- Python 
- FastAPI
- SQLModel
- MySQL (con Docker)
- JWT (Autenticación)
- Pydantic v2
- Uvicorn
- MySQL Connector
- Passlib (bcrypt)
- Multipart/form-data (para subir imágenes)
- Python-dotenv

---

## 📁 Estructura del proyecto

app/
├── main.py # Punto de entrada de la app
├── models/ # Modelos SQLModel
│ └── models.py
├── schemas/ # Esquemas Pydantic
│ └── schemas.py
├── crud/ # Lógica CRUD
│ └── leyendas.py
├── routes/ # Rutas agrupadas (auth, leyendas)
│ ├── auth.py
│ └── leyendas.py
├── auth/ # Manejo de autenticación JWT
│ └── auth.py
├── db/ # Conexión y configuración de la base de datos
│ ├── db.py
│ └── config.py
├── utils/ # Funciones auxiliares
│ └── images.py
sql_scripts/
├── create_db.sql # Script de inicialización de la base de datos
.env # Variables de entorno
requirements.txt
README.md


## ⚙️ Configuración

### 1. Clonar el repositorio

## 2. Crear y activar entorno virtual
  -python -m venv venv
  -source venv/bin/activate       # En Linux/macOS
# o
--.\venv\Scripts\activate        # En Windows
## 3. Instalar dependencias
  -pip install -r requirements.txt

## 4. Configurar archivo .env
Crea un archivo .env con el siguiente contenido:

##env
  -DB_LINK=tu direccion a la base de datos 
  -SECRET_KEY=tu_secreto_super_seguro
  -ALGORITHM=HS256
  -ACCESS_TOKEN_EXPIRE_MINUTES=30


## 5 Ejecutar el proyecto
  -uvicorn app.main:app --reload --port 8080
  -Documentación automática
  -Swagger UI: http://localhost:8080/docs

  -Redoc: http://localhost:8080/redoc

🔐 Autenticación
Registro: POST /users/

Login: POST /login

Enviar token por:
Header:
Authorization: Bearer <token>


🧪 Endpoints principales
Leyendas
GET /legends/: lista con filtros (title, category_id, province_id, canton_id, district_id, start_date, end_date)

POST /legends/: crear leyenda (requiere autenticación y subir imagen)

PUT /legends/{id}: actualizar leyenda del usuario actual

DELETE /legends/{id}: eliminar leyenda del usuario actual

Ubicación
GET /provinces

GET /cantons

GET /districts

Categorías
GET /categories

🖼️ Manejo de imágenes
Las imágenes se guardan en la carpeta static/images/

Se acceden mediante URL relativas (por ejemplo: /static/images/20250703163520_imagen.jpg)

🛡️ Validaciones
Autenticación con JWT

Contraseñas hasheadas con bcrypt



