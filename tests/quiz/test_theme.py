from app.quiz.models import Theme
from tests.quiz import theme2dict
from tests.utils import ok_response


class TestThemeAddView:
    async def test_unauthorized(self, cli):
        resp = await cli.post(
            "/quiz.add_theme",
            json={
                "title": "web-development",
            },
        )
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_success(self, store, authed_cli):
        theme_by_id = await store.quizzes.get_theme_by_id(1)
        assert theme_by_id is None
        themes = await store.quizzes.list_themes()
        assert len(themes) == 0

        resp = await authed_cli.post(
            "/quiz.add_theme",
            json={
                "title": "web-development",
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data=theme2dict(Theme(id=data["data"]["id"], title="web-development")),
        )
        theme_by_id = await store.quizzes.get_theme_by_id(data["data"]["id"])
        assert theme_by_id is not None
        theme_by_title = await store.quizzes.get_theme_by_title("web-development")
        assert theme_by_title is not None

        assert theme_by_id.id == theme_by_title.id
        assert theme_by_id.title == theme_by_title.title

        themes = await store.quizzes.list_themes()
        assert len(themes) == 1

    async def test_missing_title(self, authed_cli):
        resp = await authed_cli.post("/quiz.add_theme", json={})
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"
        assert data["data"]["title"][0] == "Missing data for required field."

    async def test_different_method(self, authed_cli):
        resp = await authed_cli.get("/quiz.add_theme", json={})
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"

    async def test_conflict(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/quiz.add_theme",
            json={
                "title": theme_1.title,
            },
        )
        assert resp.status == 409
        data = await resp.json()
        assert data["status"] == "conflict"


class TestThemeList:
    async def test_unauthorized(self, cli):
        resp = await cli.get("/quiz.list_themes")
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_empty(self, authed_cli):
        resp = await authed_cli.get("/quiz.list_themes")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"themes": []})

    async def test_one(self, authed_cli, theme_1):
        resp = await authed_cli.get("/quiz.list_themes")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"themes": [theme2dict(theme_1)]})

    async def test_several(self, authed_cli, theme_1, theme_2):
        resp = await authed_cli.get("/quiz.list_themes")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data={"themes": [theme2dict(theme_1), theme2dict(theme_2)]}
        )

    async def test_different_method(self, authed_cli):
        resp = await authed_cli.post("/quiz.list_themes")
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"


class TestIntegration:
    async def test_success(self, authed_cli):
        resp = await authed_cli.post(
            "/quiz.add_theme",
            json={
                "title": "integration",
            },
        )
        assert resp.status == 200
        data = await resp.json()
        theme_id = data["data"]["id"]

        resp = await authed_cli.get("/quiz.list_themes")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data={"themes": [theme2dict(Theme(id=theme_id, title="integration"))]}
        )
