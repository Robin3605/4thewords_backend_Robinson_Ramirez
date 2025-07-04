from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Body
from sqlmodel import Session
from typing import List
from app.db.db import get_session
from app.models.models import User
from app.schemas.schemas import Legend, LegendCreate, LegendUpdate, CategoryBase, ProvinceBase, CantonBase, DistrictBase, LegendOut
from app.auth.auth import get_current_user
from app.utils.images import save_uploaded_file, relative_date
from app.crud import leyendas as crud
import os
from fastapi import Form
from app.schemas.schemas import LegendUpdate, Legend as LegendSchema
from app.crud.leyendas import get_legend, update_legend as update_legend_db

router = APIRouter(prefix="/legends", tags=["Leyendas"])

@router.post("/", response_model=Legend)
def create_legend(
    title: str = Form(...),
    description: str = Form(...),
    legend_date: str = Form(...),
    category_id: int = Form(...),
    province_id: int = Form(...),
    canton_id: int = Form(...),
    district_id: int = Form(...),
    file: UploadFile = File(...),
    # file: str = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    image_url = save_uploaded_file(file)
    legend_data = LegendCreate(
        title=title,
        description=description,
        legend_date=legend_date,
        category_id=category_id,
        province_id=province_id,
        canton_id=canton_id,
        district_id=district_id
    )
    return crud.create_legend(session, legend_data, image_url, current_user.id)


@router.get("/", response_model=List[LegendOut])
def get_legends(
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    category_id: int = None,
    province_id: int = None,
    canton_id: int = None,
    district_id: int = None,
    start_date: str = None,
    end_date: str = None,
    session: Session = Depends(get_session)
):
    filters = {
        "title": title,
        "category_id": category_id,
        "province_id": province_id,
        "canton_id": canton_id,
        "district_id": district_id,
        "start_date": start_date,
        "end_date": end_date
    }
    legends = crud.get_legends(session, skip, limit, {k: v for k, v in filters.items() if v is not None})
    result = []
    for legend in legends:
        legend_dict = legend.dict()
        legend_dict["relative_date"] = relative_date(legend.created_at)
        result.append(LegendOut(**legend_dict))
    return result


@router.put("/{legend_id}", response_model=LegendSchema)
def update_legend(
    legend_id: int,
    updated_data: LegendUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_legend = get_legend(session, legend_id)
    if not db_legend:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    if db_legend.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    return update_legend_db(session, legend_id, updated_data)


@router.delete("/{legend_id}")
def delete_legend(
    legend_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_legend = crud.get_legend(session, legend_id)
    if not db_legend:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    if db_legend.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    if db_legend.image_url:
        try:
            os.remove(db_legend.image_url[1:])
        except:
            pass
    
    crud.delete_legend(session, legend_id)
    return {"message": "Leyenda eliminada"}


# ----- Datos relacionados -----

@router.get("/categories", response_model=List[CategoryBase])
def get_categories(session: Session = Depends(get_session)):
    return crud.get_categories(session)

@router.get("/provinces", response_model=List[ProvinceBase])
def get_provinces(session: Session = Depends(get_session)):
    return crud.get_provinces(session)

@router.get("/cantons", response_model=List[CantonBase])
def get_cantons( session: Session = Depends(get_session)):
    return crud.get_cantons(session)

@router.get("/districts", response_model=List[DistrictBase])
def get_districts(session: Session = Depends(get_session)):
    return crud.get_districts(session)