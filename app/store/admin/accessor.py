import typing
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        
        admin = Admin(id=self.app.database.next_admin_id, 
                        email=app.config.admin.email, 
                        password=app.config.admin.password)
        app.database.admins.append(admin)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        try:
            admin = next(admin for admin 
                            in self.app.database.admins 
                            if admin.email == email)
            return admin
        except StopIteration:
            return None

    async def get_by_id(self, id: int) -> Optional[Admin]:
        try:
            admin = next(admin for admin
                            in self.app.database.admins
                            if admin.id == id)
            return admin
        except StopIteration:
            return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(id=self.app.database.next_admin_id, 
                        email=email, 
                        password=password)
        self.app.database.admins.append(admin)
        return admin
