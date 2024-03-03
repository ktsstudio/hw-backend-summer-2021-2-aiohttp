import pytest
from aiohttp.test_utils import TestClient

from app.quiz.models import Answer, Question, Theme
from app.store.database.database import Database


class TestQuestionListView:
    @pytest.fixture
    async def question_1(self, database: Database, theme_1: Theme) -> Question:
        question = Question(
            id=len(database.questions) + 1,
            title="how are you?",
            theme_id=theme_1.id,
            answers=[
                Answer(title="well", is_correct=True),
                Answer(title="bad", is_correct=False),
            ],
        )
        database.questions.append(question)
        return question

    @pytest.fixture
    async def question_2(self, database: Database, theme_1: Theme) -> Question:
        question = Question(
            id=len(database.questions) + 1,
            title="are you doing fine?",
            theme_id=theme_1.id,
            answers=[
                Answer(title="yep", is_correct=True),
                Answer(title="nop", is_correct=False),
            ],
        )
        database.questions.append(question)
        return question

    async def test_unauthorized(self, cli: TestClient) -> None:
        response = await cli.get("/quiz.list_questions")
        assert response.status == 401

        data = await response.json()
        assert data["status"] == "unauthorized"

    async def test_success_no_questions(self, auth_cli: TestClient) -> None:
        response = await auth_cli.get("/quiz.list_questions")
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {"questions": []},
        }

    async def test_success_one_question(
        self, auth_cli: TestClient, question_1: Question
    ) -> None:
        response = await auth_cli.get("/quiz.list_questions")
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {
                "questions": [
                    {
                        "id": question_1.id,
                        "title": question_1.title,
                        "theme_id": question_1.theme_id,
                        "answers": [
                            {
                                "title": question_1.answers[0].title,
                                "is_correct": question_1.answers[0].is_correct,
                            },
                            {
                                "title": question_1.answers[1].title,
                                "is_correct": question_1.answers[1].is_correct,
                            },
                        ],
                    }
                ]
            },
        }

    async def test_success_several_questions(
        self, auth_cli: TestClient, question_1: Question, question_2: Question
    ) -> None:
        response = await auth_cli.get("/quiz.list_questions")
        assert response.status == 200

        data = await response.json()
        assert data == {
            "status": "ok",
            "data": {
                "questions": [
                    {
                        "id": question_1.id,
                        "title": question_1.title,
                        "theme_id": question_1.theme_id,
                        "answers": [
                            {
                                "title": question_1.answers[0].title,
                                "is_correct": question_1.answers[0].is_correct,
                            },
                            {
                                "title": question_1.answers[1].title,
                                "is_correct": question_1.answers[1].is_correct,
                            },
                        ],
                    },
                    {
                        "id": question_2.id,
                        "title": question_2.title,
                        "theme_id": question_2.theme_id,
                        "answers": [
                            {
                                "title": question_2.answers[0].title,
                                "is_correct": question_2.answers[0].is_correct,
                            },
                            {
                                "title": question_2.answers[1].title,
                                "is_correct": question_2.answers[1].is_correct,
                            },
                        ],
                    },
                ],
            },
        }
