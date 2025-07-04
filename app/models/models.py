from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

# ---------- Usuario ----------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    
    legends: List["Legend"] = Relationship(back_populates="owner")


# ---------- Categoría ----------
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    
    legends: List["Legend"] = Relationship(back_populates="category")


# ---------- Provincia ----------
class Province(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)


# ---------- Cantón ----------
class Canton(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    province_id: int = Field(foreign_key="province.id")
    
    province: Optional[Province] = Relationship()


# ---------- Distrito ----------
class District(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    canton_id: int = Field(foreign_key="canton.id")
    
    canton: Optional[Canton] = Relationship()


# ---------- Leyenda ----------
class Legend(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    image_url: str
    legend_date: date
    created_at: date = Field(default_factory=date.today)
    
    category_id: int = Field(foreign_key="category.id")
    province_id: int = Field(foreign_key="province.id")
    canton_id: int = Field(foreign_key="canton.id")
    district_id: int = Field(foreign_key="district.id")
    owner_id: int = Field(foreign_key="user.id")
    
    # Relaciones
    category: Optional[Category] = Relationship(back_populates="legends")
    province: Optional[Province] = Relationship()
    canton: Optional[Canton] = Relationship()
    district: Optional[District] = Relationship()
    owner: Optional[User] = Relationship(back_populates="legends")