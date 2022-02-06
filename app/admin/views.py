import json
from aiohttp.web_exceptions import (
    HTTPForbidden,
    HTTPUnauthorized,
    HTTPMethodNotAllowed,
)
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.schemes import (
    AdminSchema,
    AdminLoginRequestSchema,
    AdminLoginResponseSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminLoginRequestSchema)
    @response_schema(AdminLoginResponseSchema, 200)
    async def post(self):
        email = self.data["email"]
        password = self.data["password"]

        admin = await self.store.admins.get_by_email(email)
        if admin is None or \
            not admin.check_password(password):
            raise HTTPForbidden(
                reason="invalid password or email", 
                text=json.dumps({ "email": email, "password": password })
            )
            
        session = await new_session(request=self.request)
        session["admin_id"] = admin.id
        
        return json_response(data=AdminSchema(exclude=["password"]).dump(admin))

    async def get(self):
        raise HTTPMethodNotAllowed(method="GET", allowed_methods=["POST"])


class AdminCurrentView(View, AuthRequiredMixin):
    async def get(self):
        admin_id = await self.check_authorization()
            
        admin = await self.store.admins.get_by_id(admin_id)
        if admin is None:
            raise HTTPForbidden(
                reason="invalid authorization id"
            )
            
        return json_response(data=AdminSchema(exclude=["password"]).dump(admin))        
