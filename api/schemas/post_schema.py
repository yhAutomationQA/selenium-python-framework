from typing import Optional

from pydantic import BaseModel, Field


class CreatePostSchema(BaseModel):
    """Request schema for creating a new post."""

    title: str = Field(..., min_length=1, max_length=500)
    body: str = Field(..., min_length=1)
    user_id: int = Field(alias="userId", ge=1)

    model_config = {"populate_by_name": True}


class UpdatePostSchema(BaseModel):
    """Request schema for fully replacing a post."""

    id: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=500)
    body: str = Field(..., min_length=1)
    user_id: int = Field(alias="userId", ge=1)

    model_config = {"populate_by_name": True}


class PatchPostSchema(BaseModel):
    """Request schema for partially updating a post."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    body: Optional[str] = Field(None, min_length=1)
    user_id: Optional[int] = Field(None, alias="userId", ge=1)

    model_config = {"populate_by_name": True}
