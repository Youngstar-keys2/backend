from datetime import timedelta

from fastapi import APIRouter, Form, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.queries import registr
from app.auth.hash import get_password_hash, verify_password
from app.auth.JWTtoken import create_access_token
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

registr_router = APIRouter(tags=["Registration"])


@registr_router.post('/registration')
async def registration_user(applicant: str = Form(..., title='Имя заявителя'),
                            addres_applicant: str = Form(..., title='Аддрес заявителя'),
                            country: str = Form(..., title='страна заявителя'),
                            request: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await registr.check_auth(request.username)
    if user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with this login exists")
    if len(request.password) < 6 or request.password.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad password, password shoud be better :)")
    request.password = get_password_hash(request.password)
    await registr.create_user(applicant, addres_applicant, country, request.username, request.password)
    # generate a jwt token and return
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@registr_router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await registr.check_auth(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User doesnt exist')
    if not verify_password(request.password, user['password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
