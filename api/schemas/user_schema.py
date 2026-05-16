from typing import Optional

from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    """Request schema for creating a new user."""

    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: Optional[str] = None
    website: Optional[str] = None


class UpdateUserSchema(BaseModel):
    """Request schema for updating an existing user."""

    name: Optional[str] = Field(None, min_length=1)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: Optional[str] = None
    website: Optional[str] = None
