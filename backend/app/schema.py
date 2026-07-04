from pydantic import BaseModel,EmailStr,ConfigDict
from decimal import Decimal
from typing import Dict,Optional


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class TokenData(BaseModel):
    id:Optional[int]=None
    name:Optional[str]=None

class SaveAnswerRequest(BaseModel):
    question_id:int
    selected_option:Optional[list[str]]=None
    answer_numeric:Optional[float]=None


























