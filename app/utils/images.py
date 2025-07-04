import os
from fastapi import UploadFile
from datetime import datetime

# -----------------------------
# FUNCIONES PARA GUARDAR IMAGEN
# -----------------------------

def save_uploaded_file(file: UploadFile, upload_dir: str = "app/static/images") -> str:
    # Crear el directorio si no existe
    os.makedirs(upload_dir, exist_ok=True)

    # Agregar timestamp al nombre para evitar colisiones
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    # Guardar el archivo en disco
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Retornar la URL relativa que se guarda en la base de datos
    return f"/static/images/{filename}"


# -----------------------------
# FUNCIONES PARA FECHA RELATIVA
# -----------------------------

def relative_date(target_date: datetime.date) -> str:
    today = datetime.now().date()
    delta = today - target_date

    if delta.days == 0:
        return "Hoy"
    elif delta.days == 1:
        return "Ayer"
    elif delta.days < 7:
        return f"Hace {delta.days} días"
    elif delta.days < 30:
        weeks = delta.days // 7
        return f"Hace {weeks} semana{'s' if weeks > 1 else ''}"
    elif delta.days < 365:
        months = delta.days // 30
        return f"Hace {months} mes{'es' if months > 1 else ''}"
    else:
        years = delta.days // 365
        return f"Hace {years} año{'s' if years > 1 else ''}"