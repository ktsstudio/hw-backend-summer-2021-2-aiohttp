from typing import Optional
from aiohttp_session import get_session
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPUnauthorized

from app.web.utils import error_json_response


class AuthRequiredMixin:
    async def check_authorization(self):
        session = await get_session(self.request)

        id = session.get('admin_id', None)
        if id is None:
            raise HTTPUnauthorized(reason='authorization required to proceed', 
                                    text='{}')