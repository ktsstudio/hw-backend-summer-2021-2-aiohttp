from dataclasses import asdict
from typing import Optional, Union

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class DuplicationError(Exception):
    pass


class ConsistencyError(Exception):
    pass


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        try:
            theme = next(theme for theme
                            in self.app.database.themes 
                            if theme.title == title)
            return theme
        except StopIteration:
            return None

    async def get_theme_by_id(self, id: int) -> Optional[Theme]:
        try:
            theme = next(theme for theme
                            in self.app.database.themes
                            if theme.id == id)
            return theme
        except StopIteration:
            return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes[:]

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        try:
            question = next(question for question
                            in self.app.database.questions
                            if question.title == title)
            return question
        except StopIteration:
            return None

    async def create_question(self, 
        title: str, theme_id: int, answers: list[Union[dict, Answer]]
    ) -> Question:
        theme = await self.get_theme_by_id(theme_id)
        if theme is None:
            raise ConsistencyError("there is no theme with such id",
                                    {
                                        "title": title,
                                        "theme_id": theme_id
                                    })

        duplicate_question = await self.get_question_by_title(title)
        if duplicate_question is not None:
            raise DuplicationError("there is a question with such title already",
                                    {
                                        "title": title,
                                        "duplicate": asdict(duplicate_question)
                                    })
        
        if answers and not isinstance(answers[0], Answer):
            answers = [Answer(**answer) for answer in answers]

        question = Question(
            id=self.app.database.next_question_id, 
            title=title,
            theme_id=theme_id,
            answers=answers,
        )
        
        self.app.database.questions.append(question)
        return question

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        if theme_id is None:
            return self.app.database.questions[:]
        else:
            theme = await self.get_theme_by_id(theme_id)
            if theme is None:
                raise ConsistencyError("there is no theme with such id",
                                        {
                                            "theme_id": theme_id
                                        })
            return [question for question
                    in self.app.database.questions 
                    if question.theme_id == theme_id]
