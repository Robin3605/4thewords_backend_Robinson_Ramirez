from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Body
from sqlmodel import Session, select
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
from app.models.models import Canton, District
from app.schemas.schemas import ProvinceRead, CantonRead, DistrictRead, CategoryRead
from sqlalchemy.orm import selectinload
from datetime import date
from app.schemas.schemas import Legend as LegendSchema, LegendOut
from app.models.models import Legend as LegendModel
from fastapi import Request


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
    request: Request = None,
    session: Session = Depends(get_session),
    
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
        legend_dict["image_url"] = str(request.base_url)[:-1] + legend.image_url
        legend_dict["category"] = legend.category.dict() if legend.category else None
        legend_dict["province"] = legend.province.dict() if legend.province else None
        legend_dict["canton"] = legend.canton.dict() if legend.canton else None
        legend_dict["district"] = legend.district.dict() if legend.district else None
        legend_dict["relative_date"] = relative_date(legend.created_at)
        result.append(legend_dict)
    return result


@router.get("/{id}", response_model=LegendOut)
def get_legend_by_id(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    legend = session.get(LegendModel, id)
    if not legend:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    
    if legend.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta leyenda")

   
    today = date.today()
    years = today.year - legend.legend_date.year
    relative_date = f"hace {years} años" if years > 0 else "este año"

    return {
        **legend.dict(),
        "image_url": f"http://localhost:8080{legend.image_url}",
        "relative_date": relative_date
    }

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


