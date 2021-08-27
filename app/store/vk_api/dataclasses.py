from dataclasses import dataclass


# Базовые структуры, для выполнения задания их достаточно,
# поэтому постарайтесь не менять их пожалуйста из-за возможных проблем с тестами
@dataclass
class Message:
    user_id: int
    text: str


@dataclass
class UpdateMessage:
    from_id: int
    text: str
    id: int


@dataclass
class UpdateObject:
    message: UpdateMessage


@dataclass
class Update:
    type: str
    object: UpdateObject
