import json
from aiohttp_apispec import request_schema, response_schema
from aiohttp.web_exceptions import (
    HTTPConflict,
    HTTPMethodNotAllowed,
)

from app.quiz.schemes import (
    ThemeListSchema,
    ThemeSchema,
    ThemeAddRequestSchema,
    ThemeAddResponseSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


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


class ThemeListView(View, AuthRequiredMixin):
    async def get(self):
        await self.check_authorization()

        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))

    async def post(self):
        raise HTTPMethodNotAllowed(method='POST', allowed_methods=['GET'])


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
