
from fastapi import APIRouter
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from .. import dependencies as deps

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




@router.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(deps.get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/users/{user_id}/items/", response_model=List[schemas.Item])
async def get_items_for_user(
        user_id: int, db: Session = Depends(deps.get_db),
        skip: int = 0, limit: int = 5,
    ):
    return crud.get_user_items(db=db, user_id=user_id,skip=skip, limit=limit)
