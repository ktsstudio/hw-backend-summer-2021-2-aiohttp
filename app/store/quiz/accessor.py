from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        raise NotImplementedError

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        raise NotImplementedError

    async def list_themes(self) -> list[Theme]:
        raise NotImplementedError

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        raise NotImplementedError

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        raise NotImplementedError

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        raise NotImplementedError
