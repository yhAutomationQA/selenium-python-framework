from pydantic import BaseModel, Field


class PostModel(BaseModel):
    """JSONPlaceholder post resource."""

    id: int = Field(..., ge=1)
    user_id: int = Field(alias="userId", ge=1)
    title: str
    body: str

    model_config = {"populate_by_name": True}
