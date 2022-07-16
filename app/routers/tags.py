from typing import List
from fastapi import APIRouter, Path, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from app.auth.oauth2 import get_current_user
from app.db.redis import Redis
from app.queries import tags

tags_router = APIRouter(tags=["Tags"])


@tags_router.get("/tags")
async def get_all_tags(
    current_user: str = Depends(get_current_user),
    category: str = Query(..., description="Название категории"),
    page: int = Query(..., description="страница"),
) -> JSONResponse:
    back = await tags.get_tags(category, page)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"tags": [dict(**x) for x in back]},
    )


@tags_router.get("/search")
async def get_seek(
    list: List[str] = Query(..., description="Cписок тэгов"),
    page: int = Query(..., description="страница"),
):
    back = await tags.seek_tags_info(list, page)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"tags": [dict(**x) for x in back]},
    )
