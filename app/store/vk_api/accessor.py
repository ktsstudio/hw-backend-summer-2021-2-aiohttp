import typing
from typing import Optional

from aiohttp.client import ClientSession, TCPConnector

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import (Update, Message)
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    API_SERVER = "https://api.vk.com/method"

    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.session: Optional[ClientSession] = None
        
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.ts: Optional[int] = None

        self.poller: Optional[Poller] = None

        # костыль для прохождения тестов
        self.connected = False

    @staticmethod
    def _build_query(server: str, api_method: str, params: dict) -> str:
        params.setdefault("v", "5.131")

        url = f"{server}/{api_method}?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_server(self):
        api_method = "groups.getLongPollServer"
        params = {
            "access_token": self.app.config.bot.token,
            "group_id": self.app.config.bot.group_id,
            "v": "5.131",
        }

        query_url = self._build_query(VkApiAccessor.API_SERVER, api_method, params)
        async with self.session.get(query_url) as response:
            json = await response.json()
            data = json["response"]

        return data["key"], data["server"], data["ts"]

    async def connect(self, app: "Application"):
        await super().connect(app)
        # костыль для прохождения тестов
        self.connected = True

        self.session = ClientSession(connector=TCPConnector(ssl=False))
        try:
            self.key, self.server, self.ts = await self._get_long_poll_server()
            self.poller = Poller(self.app.store)
            await self.poller.start()
        except RuntimeError as e:
            # it's worth to add logging
            self.session.close()

    async def disconnect(self, app: "Application"):
        if self.connected: # костыль для прохождения тестов
            self.poller.stop()
            self.session.close()

    async def poll(self) -> list[Update]:
        server = self.server
        params = {
            "act": "a_check",
            "key": self.key,
            "ts": self.ts,
            "wait": 25,     # recommended value
        }

        query_url = f"{server}?" + \
                    "&".join([f"{k}={v}" for k, v in params.items()])

        async with self.session.get(query_url) as response:
            json = await response.json()
            data = json["response"]

            self.ts = int(data["ts"])
            updates = data["updates"]
        
        return [Update(update) for update in updates]

    async def send_message(self, message: Message) -> None:
        api_method = "messages.send"
        params = {
            "access_token": self.app.config.bot.token,
            "user_id": message.user_id,
            "message": message.text,
        }
        query_url = self._build_query(VkApiAccessor.API_SERVER, api_method, params)

        async with self.session.get(query_url) as response:
            json = await response.json()
            if not "error" in json:
                sent_message_id = int(json["response"])
            else:
                error_message = json["error"]["error_msg"]
                raise RuntimeError(error_message)

