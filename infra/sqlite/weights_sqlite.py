from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from core.errors import WeightRecordAlreadyExistsError
from core.weight_records import WeightRecord
from infra.sqlite.database_sqlite import SqliteDatabase


@dataclass
class WeightsSqlite:
    sqlite_database: SqliteDatabase

    def create(self, weight_record: WeightRecord) -> None:
        self._check_exists(weight_record.get_id())

        record_id = weight_record.get_id()
        username = weight_record.get_username()
        weight = weight_record.get_weight()
        date = weight_record.get_date()

        query = (
            "INSERT INTO main.weight_records (ID, USERNAME, WEIGHT, DATE)"
            "VALUES (?, ?, ?, ?);"
        )
        params = (record_id, username, weight, date)

        self.sqlite_database.execute(query, params)

    def get_by_username(self, username: str) -> list[WeightRecord]:
        query = "SELECT * FROM weight_records WHERE username = ?"
        params = (username,)

        result = self.sqlite_database.fetch_all(query, params)

        return [
            WeightRecord(id=r[0], username=r[1], weight=r[2], date=r[3]) for r in result
        ]

    def get_latest(self, username: str) -> WeightRecord | None:
        query = "SELECT * FROM weight_records WHERE username = ? ORDER BY date DESC LIMIT 1"
        params = (username,)

        r = self.sqlite_database.fetch_one(query, params)

        return WeightRecord(id=r[0], username=r[1], weight=r[2], date=r[3])

    def delete(self, record_id: UUID) -> None:
        query = "DELETE FROM weight_records WHERE ID = ?"
        params = (record_id,)

        self.sqlite_database.execute(query, params)

    def _check_exists(self, record_id: UUID) -> None:
        query = "SELECT ID FROM goals WHERE ID = ?"
        params = (record_id,)
        result = self.sqlite_database.fetch_one(query, params)

        if result is not None:
            raise WeightRecordAlreadyExistsError(record_id)
