from __future__ import annotations

from dataclasses import dataclass, field

from core.auth import hash_password
from core.errors import UserAlreadyExistsError, UserDoesNotExistError
from core.users import User


@dataclass
class UsersInMemory:
    users: dict[str, User] = field(default_factory=dict)

    def create(self, user: User) -> None:
        if user.get_username() in self.users.keys():
            raise UserAlreadyExistsError(user.get_username())

        self.users[user.get_username()] = user

    def get_by_username(self, username: str) -> User | None:
        if username not in self.users.keys():
            raise UserDoesNotExistError(username)

        return self.users[username]

    def update_password(self, username: str, new_password: str) -> None:
        if username not in self.users.keys():
            raise UserDoesNotExistError(username)

        self.users[username].set_password(hash_password(new_password))
