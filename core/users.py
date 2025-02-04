from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class User:
    username: str
    password: str

    def get_username(self) -> str:
        return self.username

    def get_password(self) -> str:
        return self.password

    def set_username(self, username: str) -> None:
        self.username = username

    def set_password(self, password: str) -> None:
        self.password = password


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        pass

    def get_by_username(self, username: str) -> User | None:
        pass

    def update_password(self, username: str, new_password: str) -> None:
        pass
