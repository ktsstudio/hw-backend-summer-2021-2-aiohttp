import json
from aiohttp_apispec import docs, querystring_schema, request_schema, response_schema
from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPNotFound,
    HTTPConflict,
    HTTPMethodNotAllowed,
)

from app.quiz.schemes import (
    QuestionListQuerystringSchema,
    ThemeSchema,
    ThemeListSchema,
    ThemeAddRequestSchema,
    QuestionSchema,
    QuestionListSchema,
    QuestionAddRequestSchema,
)
from app.store.quiz.accessor import DuplicationError, ConsistencyError
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(View, AuthRequiredMixin):
    @docs(
        tags=["quiz"],
        summary="Add new quiz theme",
        description="Add new theme for the quiz",
        responses={
            200: {"description": "Added quiz theme", "schema": ThemeSchema},
            409: {"description": "Theme already exists"},
        },
    )
    @request_schema(ThemeAddRequestSchema)
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
    @docs(
        tags=["quiz"],
        summary="Show quiz themes list",
        description="Show all added quiz themes",
        responses={
            200: {"description": "All added quiz themes", "schema": ThemeListSchema},
        },
    )
    async def get(self):
        await self.check_authorization()

        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))

    async def post(self):
        raise HTTPMethodNotAllowed(method="POST", allowed_methods=["GET"])


class QuestionAddView(View, AuthRequiredMixin):
    @docs(
        tags=["quiz"],
        summary="Add new quiz question",
        description="Add new question for the quiz",
        responses={
            200: {"description": "Added quiz question", "schema": QuestionSchema},
            400: {"description": "Bad question answers"},
            404: {"description": "No such quiz theme"},
            409: {"description": "Question already exists"},
        },
    )    
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
    @docs(
        tags=["quiz"],
        summary="Show quiz questions list",
        description="Show added quiz questions, optionally filtered by theme id",
        responses={
            200: {"description": "All added quiz questions", "schema": QuestionListSchema},
        },
    )   
    @querystring_schema(QuestionListQuerystringSchema)
    async def get(self):
        await self.check_authorization()

        params = self.request['querystring']
        theme_id = int(params.get("theme_id", 0)) or None

        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(data=QuestionListSchema().dump({"questions": questions}))
        
    async def post(self):
        raise HTTPMethodNotAllowed(method="POST", allowed_methods=["GET"])
