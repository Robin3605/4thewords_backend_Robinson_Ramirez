from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from app.db.db import get_session
from app.models.models import Canton, District
from app.schemas.schemas import ProvinceRead, CantonRead, DistrictRead, CategoryRead
from app.crud import leyendas as crud
from typing import List

router = APIRouter(prefix="/legends", tags=["Leyendas Públicas"])

@router.get("/categories", response_model=List[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    return crud.get_categories(session)

@router.get("/provinces", response_model=List[ProvinceRead])
def get_provinces(session: Session = Depends(get_session)):
    return crud.get_provinces(session)

@router.get("/cantons", response_model=List[CantonRead])
def get_cantons(province_id: int = Query(...), session: Session = Depends(get_session)):
    return session.exec(select(Canton).where(Canton.province_id == province_id)).all()

@router.get("/districts", response_model=List[DistrictRead])
def get_districts(canton_id: int = Query(...), session: Session = Depends(get_session)):
    return session.exec(select(District).where(District.canton_id == canton_id)).all()