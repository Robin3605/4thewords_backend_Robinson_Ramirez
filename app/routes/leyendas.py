from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.db import get_session
from app.models.models import User
from app.schemas.schemas import Legend, CreatingLegend, LegendUpdate, LegendOut
from app.auth.auth import get_current_user
# from app.utils.images import save_uploaded_file, relative_date
from app.crud import leyendas as crud
import os
from fastapi import Form
from app.schemas.schemas import LegendUpdate, Legend as LegendSchema
# from app.crud.leyendas import get_legend, update_legend as update_legend_db
# from app.models.models import Canton, District
# from app.schemas.schemas import ProvinceRead, CantonRead, DistrictRead, CategoryRead
# from sqlalchemy.orm import selectinload
# from datetime import date
from app.schemas.schemas import Legend as LegendSchema, LegendOut
# from app.models.models import Legend as LegendModel
from fastapi import Request
from app.crud.legends import creating_legend, get_legend_by_id, update_legend, delete_legend, get_legends
from app.utils.utils import QueryParams


router = APIRouter(prefix="/legends", tags=["Leyendas"])

@router.post("/", response_model=Legend)
def created_legend(data: CreatingLegend = Depends(),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    return creating_legend(data, session, current_user)
# def create_legend(
#     title: str = Form(...),
#     description: str = Form(...),
#     legend_date: str = Form(...),
#     category_id: int = Form(...),
#     province_id: int = Form(...),
#     canton_id: int = Form(...),
#     district_id: int = Form(...),
#     file: UploadFile = File(...),
#     # file: str = File(...),
#     session: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     image_url = save_uploaded_file(file)
#     legend_data = LegendCreate(
#         title=title,
#         description=description,
#         legend_date=legend_date,
#         category_id=category_id,
#         province_id=province_id,
#         canton_id=canton_id,
#         district_id=district_id
#     )
#     return crud.create_legend(session, legend_data, image_url, current_user.id)


@router.get("/", response_model=List[LegendOut])
def get_legends_created(
    skip: int = 0,
    limit: int = 100,
    query: QueryParams = Depends(),
    request: Request = None,
    session: Session = Depends(get_session),
    
):
    return get_legends(query, session, request, skip, limit)


@router.get("/{id}", response_model=LegendOut)
def get_legend_id(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return get_legend_by_id(id, session, current_user)

@router.put("/{legend_id}", response_model=LegendSchema)
def update_legends(
    legend_id: int,
    updated_data: LegendUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return update_legend(legend_id, updated_data, session, current_user)


@router.delete("/{legend_id}")
def delete_legends(
    legend_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    delete_legend(legend_id, session, current_user)
    return {"message": "Leyenda eliminada"}


