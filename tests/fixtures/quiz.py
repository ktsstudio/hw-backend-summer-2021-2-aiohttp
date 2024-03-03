import pytest

from app.quiz.models import Theme
from app.store.database.database import Database


@pytest.fixture
async def theme_1(database: Database) -> Theme:
    theme = Theme(id=len(database.themes) + 1, title="web-development")
    database.themes.append(theme)
    return theme
