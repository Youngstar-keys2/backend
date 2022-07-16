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


class FormForNeiro(UserReg):
    number: str = Form(..., description="тралял тополя")
    il: str = Form(..., description="тралял тополя")
    izgotovitel: str = Form(..., description="тралял тополя")
    addres_izgot: str = Form(..., description="тралял тополя")


class OutputNeiro(BaseModel):
    group: str
    tex_regl: str
    code: int
