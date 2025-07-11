from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from fastapi import Form, UploadFile, File
# from app.db.db import get_session
# from app.auth.auth import get_current_user
# from sqlmodel import  Session
# from app.models.models import  User



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

class CreatingLegend:
    def __init__(
        self,
        title: str = Form(...),
        description: str = Form(...),
        legend_date: str = Form(...),
        category_id: int = Form(...),
        province_id: int = Form(...),
        canton_id: int = Form(...),
        district_id: int = Form(...),
        file: UploadFile = File(...)
    ):
        self.title = title
        self.description = description
        self.legend_date = legend_date
        self.category_id = category_id
        self.province_id = province_id
        self.canton_id = canton_id
        self.district_id = district_id
        self.file = file
   



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
    
    relative_date: Optional[str] = None  

    class Config:
        from_attributes = True
        orm_mode = True



    class Config:
        from_attributes = True


class ProvinceBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class CantonBase(BaseModel):
    id: int
    name: str
    province_id: int

    class Config:
        from_attributes = True

class DistrictBase(BaseModel):
    id: int
    name: str
    canton_id: int

    class Config:
        from_attributes = True




class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
    



class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True




class ProvinceRead(ProvinceBase):
    id: int

    class Config:
        from_attributes = True


class CantonRead(CantonBase):
    id: int

    class Config:
        from_attributes = True


class DistrictRead(DistrictBase):
    id: int

    class Config:
        from_attributes = True


class LegendOut(BaseModel):
    id: int
    title: str
    description: str
    image_url: Optional[str]
    legend_date: date
    created_at: date
    relative_date: str
    owner_id: int
    category: Optional[CategoryRead] = None
    province: Optional[ProvinceRead] = None
    canton: Optional[CantonRead] = None
    district: Optional[DistrictRead] = None

    class Config:
        orm_mode = True