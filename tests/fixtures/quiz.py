import pytest

from app.quiz.models import Answer, Question, Theme


@pytest.fixture
async def theme_1(store) -> Theme:
    return await store.quizzes.create_theme(title="web-development")


@pytest.fixture
async def theme_2(store) -> Theme:
    return await store.quizzes.create_theme(title="backend")


@pytest.fixture
async def question_1(store, theme_1) -> Question:
    return await store.quizzes.create_question(
        title="how are you?",
        theme_id=theme_1.id,
        answers=[
            Answer(
                title="well",
                is_correct=True,
            ),
            Answer(
                title="bad",
                is_correct=False,
            ),
        ],
    )


@pytest.fixture
async def question_2(store, theme_1) -> Question:
    return await store.quizzes.create_question(
        title="are you doing fine?",
        theme_id=theme_1.id,
        answers=[
            Answer(
                title="yep",
                is_correct=True,
            ),
            Answer(
                title="nop",
                is_correct=False,
            ),
        ],
    )
