from sqlmodel import select, Session
from datetime import date
from typing import Optional, List
from app.models.models import Legend, Category, Province, Canton, District
from app.schemas.schemas import LegendCreate, LegendUpdate
from sqlalchemy.orm import selectinload



def create_legend(session: Session, legend: LegendCreate, image_url: str, user_id: int) -> Legend:
    db_legend = Legend(**legend.dict(), image_url=image_url, owner_id=user_id)
    session.add(db_legend)
    session.commit()
    session.refresh(db_legend)
    return db_legend


def get_legend(session: Session, legend_id: int) -> Optional[Legend]:
    return session.get(Legend, legend_id)


def update_legend(session, legend_id: int, legend: LegendUpdate):
    db_legend = session.get(Legend, legend_id)
    if not db_legend:
        return None
    legend_data = legend.dict(exclude_unset=True)
    for key, value in legend_data.items():
        setattr(db_legend, key, value)
    session.add(db_legend)
    session.commit()
    session.refresh(db_legend)
    return db_legend


def delete_legend(session: Session, legend_id: int) -> bool:
    db_legend = session.get(Legend, legend_id)
    if db_legend:
        session.delete(db_legend)
        session.commit()
        return True
    return False


def get_legends(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    filters: dict = {}
) -> List[Legend]:
    query = select(Legend).options(
        selectinload(Legend.category),
        selectinload(Legend.province),
        selectinload(Legend.canton),
        selectinload(Legend.district),
    )

    if "title" in filters:
        query = query.where(Legend.title.contains(filters["title"]))
    
    if "category_id" in filters:
        query = query.where(Legend.category_id == filters["category_id"])
    
    if "province_id" in filters:
        query = query.where(Legend.province_id == filters["province_id"])
    
    if "canton_id" in filters:
        query = query.where(Legend.canton_id == filters["canton_id"])
    
    if "district_id" in filters:
        query = query.where(Legend.district_id == filters["district_id"])
    
    if "start_date" in filters and "end_date" in filters:
        query = query.where(
            Legend.legend_date.between(filters["start_date"], filters["end_date"])
        )

    return session.exec(query.offset(skip).limit(limit)).all()

def get_categories(session: Session):
    return session.exec(select(Category)).all()


def get_provinces(session: Session):
    return session.exec(select(Province)).all()


def get_cantons(session: Session):
    return session.exec(select(Canton)).all()


def get_districts(session: Session):
    return session.exec(select(District)).all()