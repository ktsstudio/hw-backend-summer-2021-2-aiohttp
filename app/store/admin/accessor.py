import typing

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        # TODO: создать админа по данным в config.yml здесь
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Admin | None:
        raise NotImplementedError

    async def create_admin(self, email: str, password: str) -> Admin:
        raise NotImplementedError
