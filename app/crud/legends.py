from sqlmodel import  Session
from datetime import date
from app.models.models import  User
from app.schemas.schemas import LegendCreate, LegendUpdate
from fastapi import  HTTPException, Request
from app.utils.images import save_uploaded_file
from app.repository.legends import create, get_one, update_one, delete_one, get_all_legends, get_all_categories, get_all_provinces, get_all_cantons, get_all_districts
from app.schemas.schemas import CreatingLegend
import os
from app.utils.utils import QueryParams
from app.utils.images import  relative_date



def creating_legend(data: CreatingLegend , session: Session, user: User):
    image_url = save_uploaded_file(data.file)
    legend_data = LegendCreate(
        title=data.title,
        description=data.description,
        legend_date=data.legend_date,
        category_id=data.category_id,
        province_id=data.province_id,
        canton_id=data.canton_id,
        district_id=data.district_id
    )
    return create(session, legend_data, image_url, user.id)



def get_legend_by_id(id: int, session: Session , current_user: User ):
    legend = get_one(session, id)
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



def update_legend(
    legend_id: int,
    updated_data: LegendUpdate,
    session: Session ,
    current_user: User 
):
    db_legend = get_one(session, legend_id)
    if not db_legend:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    if db_legend.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    return update_one(legend_id, updated_data, session)



def delete_legend(
    legend_id: int,
    session: Session ,
    current_user: User 
):
    db_legend = get_one(session, legend_id)
    if not db_legend:
        raise HTTPException(status_code=404, detail="Leyenda no encontrada")
    if db_legend.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    if db_legend.image_url:
        try:
            os.remove(db_legend.image_url[1:])
        except:
            pass
    
    delete_one(session, legend_id)
    return {"message": "Leyenda eliminada"}




def get_legends(query: QueryParams, session: Session, request: Request, skip: int = 0, limit: int = 100):
    filters = {
        "title": query.title,
        "category_id": query.category_id,
        "province_id": query.province_id,
        "canton_id": query.canton_id,
        "district_id": query.district_id,
        "start_date": query.start_date,
        "end_date": query.end_date
    }
    legends = get_all_legends(session, skip, limit, {k: v for k, v in filters.items() if v is not None})
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
        print("📌 Filtros aplicados:", filters)
    return result

def get_categories(session: Session):
    return get_all_categories(session)


def get_provinces(session: Session):
    return get_all_provinces(session)


def get_cantons(session: Session):
    return get_all_cantons(session)


def get_districts(session: Session):
    return get_all_districts(session)