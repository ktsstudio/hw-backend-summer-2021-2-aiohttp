from app.quiz.models import Question, Answer
from tests.quiz import question2dict
from tests.utils import ok_response


class TestQuestionAddView:
    async def test_success(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data=question2dict(
                Question(
                    id=data["data"]["id"],
                    title="How many legs does an octopus have?",
                    theme_id=1,
                    answers=[
                        Answer(title="2", is_correct=False),
                        Answer(title="8", is_correct=True),
                    ],
                )
            )
        )

    async def test_unauthorized(self, cli):
        resp = await cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": 1,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_theme_not_found(self, authed_cli):
        resp = await authed_cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": 1,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 404

    async def test_all_answers_are_correct(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": True,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 400

    async def test_all_answers_are_incorrect(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": False,
                    },
                ],
            },
        )
        assert resp.status == 400

    async def test_only_one_answer(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/quiz.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"


class TestQuestionListView:
    async def test_unauthorized(self, cli):
        resp = await cli.get("/quiz.list_questions")
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_empty(self, authed_cli):
        resp = await authed_cli.get("/quiz.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"questions": []})

    async def test_one_question(self, authed_cli, question_1):
        resp = await authed_cli.get("/quiz.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"questions": [question2dict(question_1)]})

    async def test_several_questions(self, authed_cli, question_1, question_2):
        resp = await authed_cli.get("/quiz.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data={"questions": [question2dict(question_1), question2dict(question_2)]}
        )
