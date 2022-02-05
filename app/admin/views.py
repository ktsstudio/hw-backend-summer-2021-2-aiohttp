from datetime import date
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.schemes import (
    AdminSchema,
    AdminLoginRequestSchema,
    AdminLoginResponseSchema,
)
from app.web.app import View
from app.web.utils import error_json_response, json_response


class AdminLoginView(View):
    @request_schema(AdminLoginRequestSchema)
    @response_schema(AdminLoginResponseSchema, 200)
    async def post(self):
        email = self.data['email']
        password = self.data['password']

        admin = await self.store.admins.get_by_email(email)
        if admin is None or \
            not admin.check_password(password):
            return error_json_response(http_status=403,
                                        message="invalid password or email", 
                                        data={ "email": email, "password": password })

        session = await new_session(request=self.request)
        session['admin_id'] = admin.id
        
        return json_response(data=AdminSchema(exclude=['password']).dump(admin))

    async def get(self):
        raise HTTPMethodNotAllowed(method='GET', allowed_methods=['POST'], text='{}')


class AdminCurrentView(View):
    async def get(self):
        session = await get_session(self.request)
        id = session.get('admin_id', None)
        if id is None:
            return error_json_response(http_status=401)
            
        admin = await self.store.admins.get_by_id(id)
        if admin is None:
            return error_json_response(http_status=403,
                                        message="invalid authorization id")
            
        return json_response(data=AdminSchema(exclude=['password']).dump(admin))        
