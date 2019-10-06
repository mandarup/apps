from fastapi import APIRouter
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .. import dependencies as deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session = Depends(deps.get_db)):
    return crud.get_item(db, item_id)
