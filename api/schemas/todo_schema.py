from typing import Optional

from pydantic import BaseModel, Field


class CreateTodoSchema(BaseModel):
    """Request schema for creating a new todo."""

    title: str = Field(..., min_length=1, max_length=500)
    completed: bool = False
    user_id: int = Field(alias="userId", ge=1)

    model_config = {"populate_by_name": True}


class UpdateTodoSchema(BaseModel):
    """Request schema for updating an existing todo."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    user_id: Optional[int] = Field(None, alias="userId", ge=1)

    model_config = {"populate_by_name": True}
