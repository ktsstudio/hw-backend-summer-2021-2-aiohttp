from app.quiz.models import Theme
from app.store import Store


class TestThemeAccessor:
    async def test_success_get_theme_by_id(
        self, store: Store, theme_1: Theme
    ) -> None:
        theme = await store.quizzes.get_theme_by_id(theme_1.id)
        assert theme == theme_1

    async def test_success_get_theme_by_title(
        self, store: Store, theme_1: Theme
    ) -> None:
        theme = await store.quizzes.get_theme_by_title(theme_1.title)
        assert theme == theme_1

    async def test_success_get_list(self, store: Store, theme_1: Theme) -> None:
        themes = await store.quizzes.list_themes()
        assert themes == [theme_1]
