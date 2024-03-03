import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app

        from app.store.admin.accessor import AdminAccessor
        from app.store.bot.manager import BotManager
        from app.store.quiz.accessor import QuizAccessor
        from app.store.vk_api.accessor import VkApiAccessor

        self.vk_api = VkApiAccessor(app)

        self.admins = AdminAccessor(app)
        self.quizzes = QuizAccessor(app)

        self.bots_manager = BotManager(app)


def setup_store(app: "Application") -> None:
    app.store = Store(app)
