from tests.utils import ok_response


class TestAdminLoginView:
    async def test_create_on_startup(self, store, config):
        admin = await store.admins.get_by_email(config.admin.email)
        assert admin is not None
        assert admin.email == config.admin.email
        # Password must be hashed
        assert admin.password != config.admin.password
        assert admin.id == 1

    async def test_success(self, cli, config):
        resp = await cli.post(
            "/admin.login",
            json={
                "email": config.admin.email,
                "password": config.admin.password,
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            {
                "id": 1,
                "email": config.admin.email,
            }
        )

    async def test_missed_email(self, cli):
        resp = await cli.post(
            "/admin.login",
            json={
                "password": "qwerty",
            },
        )
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"
        assert data["data"]["email"][0] == "Missing data for required field."

    async def test_not_valid_credentials(self, cli):
        resp = await cli.post(
            "/admin.login",
            json={
                "email": "qwerty",
                "password": "qwerty",
            },
        )
        assert resp.status == 403
        data = await resp.json()
        assert data["status"] == "forbidden"

    async def test_different_method(self, cli):
        resp = await cli.get(
            "/admin.login",
            json={
                "email": "qwerty",
                "password": "qwerty",
            },
        )
        assert resp.status == 405
        data = await resp.json()
        assert data["status"] == "not_implemented"
