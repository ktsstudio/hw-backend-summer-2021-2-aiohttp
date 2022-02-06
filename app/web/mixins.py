from aiohttp_session import get_session
from aiohttp.web_exceptions import HTTPUnauthorized


class AuthRequiredMixin:
    async def check_authorization(self) -> int:
        session = await get_session(self.request)

        admin_id = session.get("admin_id", None)
        if admin_id is None:
            raise HTTPUnauthorized(
                reason="authorization required to proceed"
            )

        return admin_id
