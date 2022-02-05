import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str
    group_id: int


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig = None
    bot: BotConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as config_file:
        raw_config = yaml.safe_load(config_file)

    app.config = Config(
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        bot=BotConfig(
            token=raw_config["bot"]["token"],
            group_id=raw_config["bot"]["group_id"],
        ),        
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
    )
