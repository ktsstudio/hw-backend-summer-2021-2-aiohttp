from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Answer:
    title: str
    is_correct: bool


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list[Answer]

    def __post_init__(self):
        if len(self.answers) < 2:
            raise ValueError("should be multiple answers", 
                                { 
                                    "title": self.title,
                                    "answers": [asdict(answer) for answer in self.answers]
                                })

        correct_answers_count = sum(answer.is_correct for answer in self.answers)
        if correct_answers_count == 0:
            raise ValueError("should be correct answer",
                                {
                                    "title": self.title,
                                    "answers": [asdict(answer) for answer in self.answers]
                                })
        elif correct_answers_count > 1:
            raise ValueError("should be only one correct answer",
                                {
                                    "title": self.title,
                                    "answers": [asdict(answer) for answer in self.answers]
                                })
