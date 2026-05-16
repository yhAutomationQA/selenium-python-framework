"""Sample integration tests for JSONPlaceholder REST API.

Uses the typed ApiClient → JSONPlaceholderService → Pydantic model
pipeline.  Run with:  pytest tests/test_jsonplaceholder_api.py
"""

import pytest

from api.client.api_client import ApiClient
from api.models.post_model import PostModel
from api.schemas.post_schema import CreatePostSchema, PatchPostSchema, UpdatePostSchema
from api.schemas.todo_schema import CreateTodoSchema
from api.schemas.user_schema import CreateUserSchema
from api.services.jsonplaceholder_service import JSONPlaceholderService

pytestmark = [pytest.mark.api, pytest.mark.integration]

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    return ApiClient(base_url=JSONPLACEHOLDER_URL, timeout=15, retry_count=1)


@pytest.fixture(scope="session")
def jsonplaceholder(api_client: ApiClient) -> JSONPlaceholderService:
    return JSONPlaceholderService(api_client)


# ── Posts ─────────────────────────────────────────────────────────


class TestPosts:
    def test_list_posts_returns_100(self, jsonplaceholder: JSONPlaceholderService):
        posts = jsonplaceholder.list_posts()
        assert len(posts) == 100
        assert all(isinstance(p, PostModel) for p in posts)

    def test_get_post_returns_typed_model(self, jsonplaceholder: JSONPlaceholderService):
        post = jsonplaceholder.get_post(1)
        assert post.id == 1
        assert post.user_id >= 1
        assert isinstance(post.title, str)
        assert isinstance(post.body, str)

    def test_get_post_has_non_empty_fields(self, jsonplaceholder: JSONPlaceholderService):
        post = jsonplaceholder.get_post(1)
        assert len(post.title) > 0
        assert len(post.body) > 0

    def test_create_post_returns_new_id(self, jsonplaceholder: JSONPlaceholderService):
        schema = CreatePostSchema(title="Test Post", body="This is a test body.", userId=1)
        created = jsonplaceholder.create_post(schema)
        assert created.id is not None
        assert created.title == "Test Post"
        assert created.body == "This is a test body."
        assert created.user_id == 1

    def test_update_post_replaces_fields(self, jsonplaceholder: JSONPlaceholderService):
        schema = UpdatePostSchema(id=1, title="Updated Title", body="Updated body.", userId=1)
        updated = jsonplaceholder.update_post(1, schema)
        assert updated.title == "Updated Title"
        assert updated.body == "Updated body."

    def test_patch_post_partial_update(self, jsonplaceholder: JSONPlaceholderService):
        schema = PatchPostSchema(title="Patched Title")
        patched = jsonplaceholder.patch_post(1, schema)
        assert patched.title == "Patched Title"

    def test_delete_post_returns_success(self, jsonplaceholder: JSONPlaceholderService):
        assert jsonplaceholder.delete_post(1) is True

    def test_post_not_found(self, jsonplaceholder: JSONPlaceholderService):
        assert jsonplaceholder.post_exists(99999) is False

    @pytest.mark.parametrize("post_id", [1, 25, 50, 75, 100])
    def test_multiple_posts_have_valid_structure(
        self, jsonplaceholder: JSONPlaceholderService, post_id: int
    ):
        post = jsonplaceholder.get_post(post_id)
        assert post.id == post_id
        assert post.user_id >= 1
        assert len(post.title) > 0

    def test_list_posts_all_have_unique_ids(self, jsonplaceholder: JSONPlaceholderService):
        posts = jsonplaceholder.list_posts()
        ids = [p.id for p in posts]
        assert len(ids) == len(set(ids))

    def test_list_posts_user_ids_in_range(self, jsonplaceholder: JSONPlaceholderService):
        posts = jsonplaceholder.list_posts()
        user_ids = {p.user_id for p in posts}
        assert user_ids.issubset({1, 2, 3, 4, 5, 6, 7, 8, 9, 10})


# ── Users ─────────────────────────────────────────────────────────


class TestUsers:
    def test_list_users_returns_10(self, jsonplaceholder: JSONPlaceholderService):
        users = jsonplaceholder.list_users()
        assert len(users) == 10

    def test_get_user_has_address(self, jsonplaceholder: JSONPlaceholderService):
        user = jsonplaceholder.get_user(1)
        assert user.name == "Leanne Graham"
        assert user.address is not None
        assert user.address.city == "Gwenborough"

    def test_get_user_has_company(self, jsonplaceholder: JSONPlaceholderService):
        user = jsonplaceholder.get_user(1)
        assert user.company is not None
        assert user.company.name == "Romaguera-Crona"

    def test_get_user_email_format(self, jsonplaceholder: JSONPlaceholderService):
        user = jsonplaceholder.get_user(1)
        assert "@" in user.email

    def test_all_users_have_unique_usernames(self, jsonplaceholder: JSONPlaceholderService):
        users = jsonplaceholder.list_users()
        usernames = [u.username for u in users]
        assert len(usernames) == len(set(usernames))

    def test_create_user(self, jsonplaceholder: JSONPlaceholderService):
        schema = CreateUserSchema(
            name="Test User",
            username="testuser",
            email="test@example.com",
        )
        created = jsonplaceholder.create_user(schema)
        assert created.name == "Test User"
        assert created.username == "testuser"

    def test_delete_user(self, jsonplaceholder: JSONPlaceholderService):
        assert jsonplaceholder.delete_user(1) is True


# ── Todos ─────────────────────────────────────────────────────────


class TestTodos:
    def test_list_todos_returns_200(self, jsonplaceholder: JSONPlaceholderService):
        todos = jsonplaceholder.list_todos()
        assert len(todos) == 200

    def test_get_todo_has_typed_fields(self, jsonplaceholder: JSONPlaceholderService):
        todo = jsonplaceholder.get_todo(1)
        assert todo.id == 1
        assert isinstance(todo.completed, bool)
        assert len(todo.title) > 0

    def test_some_todos_are_completed(self, jsonplaceholder: JSONPlaceholderService):
        todos = jsonplaceholder.list_todos()
        completed = [t for t in todos if t.completed]
        assert len(completed) > 0

    def test_some_todos_are_not_completed(self, jsonplaceholder: JSONPlaceholderService):
        todos = jsonplaceholder.list_todos()
        active = [t for t in todos if not t.completed]
        assert len(active) > 0

    def test_create_todo(self, jsonplaceholder: JSONPlaceholderService):
        schema = CreateTodoSchema(title="New Todo", userId=1, completed=False)
        created = jsonplaceholder.create_todo(schema)
        assert created.title == "New Todo"
        assert created.completed is False
        assert created.user_id == 1

    def test_delete_todo(self, jsonplaceholder: JSONPlaceholderService):
        assert jsonplaceholder.delete_todo(1) is True


# ── Client-Level Tests ────────────────────────────────────────────


class TestApiClient:
    def test_headers_environ(self, api_client: ApiClient):
        api_client.set_header("X-Custom", "test-value")
        assert api_client.session.headers.get("X-Custom") == "test-value"

    def test_auth_token(self, api_client: ApiClient):
        api_client.set_auth_token("my-token")
        assert api_client.session.headers.get("Authorization") == "Bearer my-token"

    def test_base_url_update(self, api_client: ApiClient):
        api_client.set_base_url("https://example.com")
        assert api_client.base_url == "https://example.com"

    def test_raise_for_status_ok(self):
        import requests as req
        from requests import Response
        response: Response = req.get(f"{JSONPLACEHOLDER_URL}/posts/1")
        # Should not raise
        ApiClient.raise_for_status(response)

    def test_json_body_returns_dict(self, api_client: ApiClient):
        response = api_client.get("posts/1")
        body = ApiClient.json_dict(response)
        assert isinstance(body, dict)
        assert "title" in body

    def test_json_list_returns_list(self, api_client: ApiClient):
        response = api_client.get("posts")
        data = ApiClient.json_list(response)
        assert isinstance(data, list)
        assert len(data) > 0
