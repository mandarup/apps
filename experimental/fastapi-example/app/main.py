from typing import List

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response


from .database import SessionLocal, engine
from .routers import items, users
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response




async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
