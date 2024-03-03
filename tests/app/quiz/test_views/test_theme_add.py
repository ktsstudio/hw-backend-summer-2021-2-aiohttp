from aiohttp.test_utils import TestClient

from app.quiz.models import Theme
from app.store.database.database import Database


class TestThemeAddView:
    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.post(
            "/quiz.add_theme", json={"title": "web-development"}
        )
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"

    async def test_success(
        self, auth_cli: TestClient, database: Database
    ) -> None:
        response = await auth_cli.post(
            "/quiz.add_theme", json={"title": "web-development"}
        )
        assert response.status == 200
        data = await response.json()

        assert data == {
            "status": "ok",
            "data": {
                "id": data["data"]["id"],
                "title": "web-development",
            },
        }
        assert database.themes == [Theme(1, "web-development")]

    async def test_bad_request_when_missed_title(
        self, auth_cli: TestClient
    ) -> None:
        response = await auth_cli.post("/quiz.add_theme", json={})
        assert response.status == 400

        data = await response.json()
        assert data == {
            "status": "bad_request",
            "message": "Unprocessable Entity",
            "data": {"json": {"title": ["Missing data for required field."]}},
        }

    async def test_conflict_when_theme_with_title_already_exists(
        self, auth_cli: TestClient, theme_1: Theme
    ) -> None:
        response = await auth_cli.post(
            "/quiz.add_theme", json={"title": theme_1.title}
        )
        assert response.status == 409

        data = await response.json()
        assert data["status"] == "conflict"
