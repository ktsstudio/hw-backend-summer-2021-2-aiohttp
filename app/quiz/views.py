import json
from aiohttp_apispec import request_schema, response_schema
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPConflict,
    HTTPMethodNotAllowed,
)

from app.quiz.schemes import (
    ThemeSchema,
    ThemeAddRequestSchema,
    ThemeAddResponseSchema,
    ThemeListSchema,
    QuestionSchema,
    QuestionAddRequestSchema,
    QuestionListSchema,
)
from app.store.quiz.accessor import DuplicationError, ConsistencyError
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(View, AuthRequiredMixin):
    @request_schema(ThemeAddRequestSchema)
    @response_schema(ThemeAddResponseSchema, 200)
    async def post(self):
        await self.check_authorization()

        title = self.data["title"]        
        theme = await self.store.quizzes.get_theme_by_title(title)

        if theme is not None:
            raise HTTPConflict(
                reason="theme already exists",
                text=json.dumps({ "title": title })
            )

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))

    async def get(self):
        raise HTTPMethodNotAllowed(method="GET", allowed_methods=["POST"])


class ThemeListView(View, AuthRequiredMixin):
    async def get(self):
        await self.check_authorization()

        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))

    async def post(self):
        raise HTTPMethodNotAllowed(method="POST", allowed_methods=["GET"])


class QuestionAddView(View, AuthRequiredMixin):
    @request_schema(QuestionAddRequestSchema)
    async def post(self):
        await self.check_authorization()

        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers = self.data["answers"]

        try:
            question = await self.store.quizzes.create_question(title, theme_id, answers)
            return json_response(data=QuestionSchema().dump(question))
        except ValueError as e:
            message, data = e.args
            raise HTTPBadRequest(
                reason=message,
                text=json.dumps(data)
            )
        except DuplicationError as e:
            message, data = e.args
            raise HTTPConflict(
                reason=message,
                text=json.dumps(data)
            )
        except ConsistencyError as e:
            message, data = e.args
            raise HTTPNotFound(
                reason=message,
                text=json.dumps(data)
            )
            

    async def get(self):
        raise HTTPMethodNotAllowed(method="GET", allowed_methods=["POST"])


class QuestionListView(View, AuthRequiredMixin):
    async def get(self):
        await self.check_authorization()

        params = self.request.rel_url.query
        theme_id = int(params.get("theme_id", 0)) or None

        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(data=QuestionListSchema().dump({"questions": questions}))
        
    async def post(self):
        raise HTTPMethodNotAllowed(method="POST", allowed_methods=["GET"])
