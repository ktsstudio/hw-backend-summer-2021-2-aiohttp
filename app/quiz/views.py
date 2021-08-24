from app.quiz.schemes import (
    ThemeSchema,
)
from app.web.app import View
from app.web.utils import json_response


# TODO: добавить проверку авторизации для этого View
class ThemeAddView(View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    async def post(self):
        title = (await self.request.json())[
            "title"
        ]  # TODO: заменить на self.data["title"] после внедрения валидации
        # TODO: проверять, что не существует темы с таким же именем, отдавать 409 если существует
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View):
    async def get(self):
        raise NotImplementedError


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
