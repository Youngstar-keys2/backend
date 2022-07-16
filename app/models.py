from fastapi import Form
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: Optional[str] = None


class UserReg(BaseModel):
    applicant: str = Form(..., title="Имя заявителя")
    addres_applicant: str = Form(..., title="Аддрес заявителя")
    country: str = Form(..., title="страна заявителя")
