from dataclasses import dataclass
from hashlib import sha256
from typing import Optional


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[str] = None

    def __post_init__(self):
        self.password = sha256(self.password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()
