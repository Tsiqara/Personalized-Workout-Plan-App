from __future__ import annotations

from dataclasses import dataclass

from core.errors import UserAlreadyExistsError, UserDoesNotExistError
from core.users import User
from infra.sqlite.database_sqlite import SqliteDatabase


@dataclass
class UsersSqlite:
    sqlite_database: SqliteDatabase

    def create(self, user: User) -> None:
        query = "SELECT username FROM users WHERE username = ?"
        params = (user.get_username(),)

        result = self.sqlite_database.fetch_one(query, params)

        if result is not None:
            raise UserAlreadyExistsError(user.get_username())

        username = user.get_username()
        password = user.get_password()

        query2 = "INSERT INTO users (username, password) " "VALUES (?, ?);"
        params2 = (
            username,
            password,
        )

        self.sqlite_database.execute(query2, params2)

    def get_by_username(self, username: str) -> User | None:
        query = "SELECT * FROM users WHERE username = ?"
        params = (username,)

        result = self.sqlite_database.fetch_one(query, params)

        if result is None:
            raise UserDoesNotExistError(username)

        username = result[0]
        password = result[1]

        return User(username, password)

    def update_password(self, username: str, new_password: str) -> None:
        user = self.get_by_username(username)

        if user is None:
            raise UserDoesNotExistError(username)

        query = "UPDATE users SET password = ? WHERE username = ?"
        params = (new_password, username)

        self.sqlite_database.execute(query, params)
