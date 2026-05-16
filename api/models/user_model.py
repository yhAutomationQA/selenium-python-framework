from typing import Optional

from pydantic import BaseModel, Field


class GeoModel(BaseModel):
    lat: str
    lng: str


class AddressModel(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Optional[GeoModel] = None


class CompanyModel(BaseModel):
    name: str
    catch_phrase: Optional[str] = Field(None, alias="catchPhrase")
    bs: Optional[str] = None


class UserModel(BaseModel):
    """JSONPlaceholder user resource."""

    id: int = Field(..., ge=1)
    name: str
    username: str
    email: str
    address: Optional[AddressModel] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[CompanyModel] = None

    model_config = {"populate_by_name": True}
