from asyncio import Task

from app.store import Store


class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        # TODO: добавить asyncio Task на запуск poll
        raise NotImplementedError

    async def stop(self) -> None:
        # TODO: gracefully завершить Poller
        raise NotImplementedError

    async def poll(self) -> None:
        raise NotImplementedError
