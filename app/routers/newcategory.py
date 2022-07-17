from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models import Newcategory
from app.queries.newcategory import add_new_category


category_router = APIRouter(tags=["Neiro"])


@category_router.post("/categorynew")
async def new_category(category: Newcategory):
    print(category)
    await add_new_category(category)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content='googd'
    )
