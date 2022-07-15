from typing import List

from fastapi import APIRouter, Path, Query, status
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse
from app.auth.oauth2 import get_current_user

tags_router = APIRouter(tags=["Tags"])


@tags_router.get('/tag')
async def get_all_tags(current_user: str = Depends(get_current_user)) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        'tags': 'hs',
        'previous_id': 'sfa',
    })
