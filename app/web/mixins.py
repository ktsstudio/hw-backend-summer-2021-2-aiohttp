import json
from aiohttp_session import get_session
from aiohttp.web_exceptions import (HTTPUnauthorized, HTTPForbidden)


class AuthRequiredMixin:
    async def check_authorization(self) -> int:
        session = await get_session(self.request)

        email = session.get("email", None)
        password = session.get("password", None)
        if email is None or password is None:
            raise HTTPUnauthorized(
                reason="authorization required to proceed"
            )
        
        admin = await self.store.admins.get_by_email(email)
        if admin is None or admin.password != password:
            raise HTTPForbidden(
                reason="invalid password or email", 
                text=json.dumps({ "email": email, "password": password })
            )

        return admin
