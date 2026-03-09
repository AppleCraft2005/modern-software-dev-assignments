from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Category
from ..schemas import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    rows = db.execute(select(Category)).scalars().all()
    return [CategoryRead.model_validate(row) for row in rows]


@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategoryRead:
    category = Category(name=payload.name)
    db.add(category)
    db.flush()
    db.refresh(category)
    return CategoryRead.model_validate(category)
