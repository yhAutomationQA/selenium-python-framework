from typing import List, Optional

from api.client.api_client import ApiClient
from api.models.post_model import PostModel
from api.models.user_model import UserModel
from api.models.todo_model import TodoModel
from api.schemas.post_schema import CreatePostSchema, PatchPostSchema, UpdatePostSchema
from api.schemas.todo_schema import CreateTodoSchema, UpdateTodoSchema
from api.schemas.user_schema import CreateUserSchema, UpdateUserSchema
from api.services.base_service import BaseService


class JSONPlaceholderService(BaseService):
    """Service for the JSONPlaceholder fake REST API (typicode).

    Provides typed CRUD operations for posts, users, and todos.
    Base URL: https://jsonplaceholder.typicode.com
    """

    def __init__(self, client: ApiClient):
        super().__init__(client)

    # ── Posts ─────────────────────────────────────────────────────

    def list_posts(self) -> List[PostModel]:
        self._resource = "posts"
        return self._list(PostModel)

    def get_post(self, post_id: int) -> PostModel:
        self._resource = "posts"
        return self._get(PostModel, post_id)

    def create_post(self, schema: CreatePostSchema) -> PostModel:
        self._resource = "posts"
        return self._create(PostModel, schema)

    def update_post(self, post_id: int, schema: UpdatePostSchema) -> PostModel:
        self._resource = "posts"
        return self._update(PostModel, post_id, schema)

    def patch_post(self, post_id: int, schema: PatchPostSchema) -> PostModel:
        self._resource = "posts"
        return self._patch(PostModel, post_id, schema)

    def delete_post(self, post_id: int) -> bool:
        self._resource = "posts"
        return self._delete(post_id)

    def post_exists(self, post_id: int) -> bool:
        self._resource = "posts"
        return self._exists(post_id)

    # ── Users ─────────────────────────────────────────────────────

    def list_users(self) -> List[UserModel]:
        self._resource = "users"
        return self._list(UserModel)

    def get_user(self, user_id: int) -> UserModel:
        self._resource = "users"
        return self._get(UserModel, user_id)

    def create_user(self, schema: CreateUserSchema) -> UserModel:
        self._resource = "users"
        return self._create(UserModel, schema)

    def update_user(self, user_id: int, schema: UpdateUserSchema) -> UserModel:
        self._resource = "users"
        return self._update(UserModel, user_id, schema)

    def delete_user(self, user_id: int) -> bool:
        self._resource = "users"
        return self._delete(user_id)

    # ── Todos ─────────────────────────────────────────────────────

    def list_todos(self) -> List[TodoModel]:
        self._resource = "todos"
        return self._list(TodoModel)

    def get_todo(self, todo_id: int) -> TodoModel:
        self._resource = "todos"
        return self._get(TodoModel, todo_id)

    def create_todo(self, schema: CreateTodoSchema) -> TodoModel:
        self._resource = "todos"
        return self._create(TodoModel, schema)

    def update_todo(self, todo_id: int, schema: UpdateTodoSchema) -> TodoModel:
        self._resource = "todos"
        return self._update(TodoModel, todo_id, schema)

    def delete_todo(self, todo_id: int) -> bool:
        self._resource = "todos"
        return self._delete(todo_id)
