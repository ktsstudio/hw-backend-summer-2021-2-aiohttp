import json
from aiohttp_apispec import request_schema, response_schema
from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPMethodNotAllowed,
)

from app.quiz.schemes import (
    ThemeSchema,
    ThemeAddRequestSchema,
    ThemeAddResponseSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class ThemeAddView(View, AuthRequiredMixin):
    @request_schema(ThemeAddRequestSchema)
    @response_schema(ThemeAddResponseSchema, 200)
    async def post(self):
        await self.check_authorization()

        title = self.data['title']
        
        theme = await self.store.quizzes.get_theme_by_title(title)
        if theme is not None:
            raise HTTPConflict(
                reason="theme already exists",
                text=json.dumps({ "title": title })
            )

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))

    async def get(self):
        raise HTTPMethodNotAllowed(method='GET', allowed_methods=['POST'])


class ThemeListView(View):
    async def get(self):
        raise NotImplementedError


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
