import os
from unittest.mock import AsyncMock

import pytest
from aiohttp.test_utils import TestClient, loop_context

from app.store import Store
from app.web.app import setup_app
from app.web.config import Config


@pytest.fixture(scope="session")
def loop():
    with loop_context() as _loop:
        yield _loop


@pytest.fixture(scope="session")
def server():
    app = setup_app(
        config_path=os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", "config.yml"
        )
    )
    app.on_startup.clear()
    app.on_shutdown.clear()
    app.store.vk_api = AsyncMock()
    app.store.vk_api.send_message = AsyncMock()
    app.on_startup.append(app.store.admins.connect)
    app.on_shutdown.append(app.store.admins.connect)
    return app


@pytest.fixture
def store(server) -> Store:
    return server.store


@pytest.fixture(autouse=True, scope="function")
def clear_db(server):
    server.database.clear()


@pytest.fixture
def config(server) -> Config:
    return server.config


@pytest.fixture(autouse=True)
def cli(aiohttp_client, loop, server) -> TestClient:
    return loop.run_until_complete(aiohttp_client(server))


@pytest.fixture
async def authed_cli(cli, config) -> TestClient:
    await cli.post(
        "/admin.login",
        json={
            "email": config.admin.email,
            "password": config.admin.password,
        },
    )
    yield cli
