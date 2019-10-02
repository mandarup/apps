
from starlette.requests import Request

# Dependency
async def get_db(request: Request):
    return request.state.db
