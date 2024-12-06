from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict
from datetime import datetime


# TRANSLATE
class TranslationRequest(BaseModel):
    content: str
    languages: List[str]


class TaskResponse(BaseModel):
    task_id: int


class TranslationResponse(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str]


class TranslationResponseContent(BaseModel):
    task_id: int
    translations: Dict[str, str]


# USERS
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password for the user")


class User(BaseModel):
    id: int = Field(..., description="ID of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    created_at: datetime = Field(...,
                                 description="Timestamp of when the user was created")


# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
