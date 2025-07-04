from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

# ---------------------------
# AUTENTICACIÓN
# ---------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str


# ---------------------------
# LEYENDAS
# ---------------------------

class LegendBase(BaseModel):
    title: str
    description: str
    legend_date: date
    category_id: int
    province_id: int
    canton_id: int
    district_id: int

class LegendCreate(LegendBase):
    pass

class LegendUpdate(LegendBase):
    pass

class Legend(LegendBase):
    id: int
    image_url: str
    created_at: date
    owner_id: int
    # opcional: agregar para mostrar la fecha relativa
    relative_date: Optional[str] = None  

    class Config:
        from_attributes = True
        orm_mode = True


# ---------------------------
# UBICACIÓN
# ---------------------------

class ProvinceBase(BaseModel):
    name: str

class CantonBase(BaseModel):
    name: str
    province_id: int

class DistrictBase(BaseModel):
    name: str
    canton_id: int


# ---------------------------
# CATEGORÍA
# ---------------------------

class CategoryBase(BaseModel):
    name: str
    

class LegendOut(Legend):
    relative_date: Optional[str] = None