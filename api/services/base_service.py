import logging
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel

from api.client.api_client import ApiClient

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseService:
    """Base class for API service objects.

    Provides common patterns: list resources, get by ID, create,
    update, delete — all returning typed Pydantic models.
    """

    def __init__(self, client: ApiClient):
        self.client = client
        self._resource: str = ""

    # ── CRUD Helpers ──────────────────────────────────────────────

    def _list(self, model_cls: Type[T], params: Optional[Dict[str, Any]] = None) -> List[T]:
        response = self.client.get(self._resource, params=params)
        data = self.client.json_list(response)
        return [model_cls.model_validate(item) for item in data]

    def _get(self, model_cls: Type[T], resource_id: int) -> T:
        response = self.client.get(f"{self._resource}/{resource_id}")
        data = self.client.json_dict(response)
        return model_cls.model_validate(data)

    def _create(self, model_cls: Type[T], schema: BaseModel) -> T:
        payload = schema.model_dump(by_alias=True, exclude_unset=True)
        response = self.client.post(self._resource, json=payload)
        data = self.client.json_dict(response)
        return model_cls.model_validate(data)

    def _update(self, model_cls: Type[T], resource_id: int, schema: BaseModel) -> T:
        payload = schema.model_dump(by_alias=True, exclude_unset=True)
        response = self.client.put(f"{self._resource}/{resource_id}", json=payload)
        data = self.client.json_dict(response)
        return model_cls.model_validate(data)

    def _patch(self, model_cls: Type[T], resource_id: int, schema: BaseModel) -> T:
        payload = schema.model_dump(by_alias=True, exclude_unset=True)
        response = self.client.patch(f"{self._resource}/{resource_id}", json=payload)
        data = self.client.json_dict(response)
        return model_cls.model_validate(data)

    def _delete(self, resource_id: int) -> bool:
        response = self.client.delete(f"{self._resource}/{resource_id}")
        return self.client.status_ok(response)

    def _exists(self, resource_id: int) -> bool:
        from requests import Response

        response: Response = self.client.get(f"{self._resource}/{resource_id}")
        return response.ok
