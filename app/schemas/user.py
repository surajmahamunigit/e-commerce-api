from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    """
    Class is inherited by UserCreate and UserResponse class/schemas
    """

    email: EmailStr


class UserCreate(UserBase):
    """
    Used for POST /auth/register endpoint
    """

    password: str


class UserResponse(UserBase):
    """
    Used for returning data after user login/register
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Used for POST /auth/login endpoint
    """

    email: EmailStr
    password: str
