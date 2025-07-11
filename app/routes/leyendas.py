from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.db import get_session
from app.models.models import User
from app.schemas.schemas import Legend, CreatingLegend, LegendUpdate, LegendOut
from app.auth.auth import get_current_user
import os
from app.schemas.schemas import LegendUpdate, Legend as LegendSchema
from app.schemas.schemas import Legend as LegendSchema, LegendOut
from fastapi import Request
from app.crud.legends import creating_legend, get_legend_by_id, update_legend, delete_legend, get_legends
from app.utils.utils import QueryParams


router = APIRouter(prefix="/legends", tags=["Leyendas"])

@router.post("/", response_model=Legend)
def created_legend(data: CreatingLegend = Depends(),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)):
    return creating_legend(data, session, current_user)


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


