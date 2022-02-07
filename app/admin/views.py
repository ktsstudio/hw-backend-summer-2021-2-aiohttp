import json
from aiohttp.web_exceptions import (
    HTTPForbidden,
    HTTPMethodNotAllowed,
)
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import (
    AdminSchema,
    AdminLoginRequestSchema,
    AdminResponseSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(
        tags=["admin"],
        summary="Log in admin",
        description="Log in a registered admin with email and password",
        responses={
            200: {"description": "Logged in", "schema": AdminResponseSchema},
            403: {"description": "Invalid password or email"},
        },
    )
    @request_schema(AdminLoginRequestSchema)
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
        session["email"] = admin.email
        session["password"] = admin.password
        
        return json_response(data=AdminSchema(exclude=["password"]).dump(admin))

    async def get(self):
        raise HTTPMethodNotAllowed(method="GET", allowed_methods=["POST"])


class AdminCurrentView(View, AuthRequiredMixin):
    @docs(
        tags=["admin"],
        summary="Show current admin",
        description="Show current session logged in admin",
        responses={
            200: {"description": "Current admin", "schema": AdminResponseSchema},
            401: {"description": "Unauthorized"},
            403: {"description": "Invalid credentials"},
        },
    )
    async def get(self):
        admin = await self.check_authorization()            
        return json_response(data=AdminSchema(exclude=["password"]).dump(admin))        
