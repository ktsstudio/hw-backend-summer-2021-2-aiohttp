from dataclasses import dataclass, field

from app.admin.models import Admin
from app.quiz.models import Theme


@dataclass
class Database:
    # TODO: добавить поле questions
    admins: list[Admin] = field(default_factory=list)
    themes: list[Theme] = field(default_factory=list)

    @property
    def next_admin_id(self) -> int:
        return len(self.admins) + 1

    @property
    def next_theme_id(self) -> int:
        return len(self.themes) + 1

    def clear(self):
        self.themes = []
