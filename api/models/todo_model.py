from pydantic import BaseModel, Field


class TodoModel(BaseModel):
    """JSONPlaceholder todo resource."""

    id: int = Field(..., ge=1)
    user_id: int = Field(alias="userId", ge=1)
    title: str
    completed: bool = False

    model_config = {"populate_by_name": True}
