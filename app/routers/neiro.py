from fastapi import APIRouter, Depends, status
from app.auth.oauth2 import get_current_user
from app.models import FormForNeiro
from fastapi.responses import JSONResponse

neiro_router = APIRouter(tags=["Neiro"])


@neiro_router.post("/neiro")
async def neiro_get(
    form: FormForNeiro,
    current_user: str = Depends(get_current_user),
):
    # получаем ответ
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="dsa",
    )
