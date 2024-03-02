from dataclasses import dataclass


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    pass


@dataclass
class Answer:
    pass
