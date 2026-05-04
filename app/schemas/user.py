import uuid
from datetime import datetime
from xxlimited import Str
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)


class UserRead(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
