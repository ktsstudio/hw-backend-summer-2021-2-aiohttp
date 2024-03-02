from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    email: str
    password: str | None = None
