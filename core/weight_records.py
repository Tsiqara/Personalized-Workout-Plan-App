from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class WeightRecord:
    username: str
    weight: float
    date: date
    id: UUID = field(default_factory=uuid4)  # Unique ID for the weight record

    def get_id(self) -> UUID:
        return self.id

    def get_username(self) -> str:
        return self.username

    def get_weight(self) -> float:
        return self.weight

    def get_date(self) -> date:
        return self.date

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def set_date(self, new_date: date) -> None:
        self.date = new_date


class WeightRecordRepository(Protocol):
    def create(self, weight_record: WeightRecord) -> None:
        pass

    def get_by_user_id(self, username: str) -> list[WeightRecord]:
        pass

    def get_latest(self, username: str) -> WeightRecord | None:
        pass

    def delete(self, record_id: UUID) -> None:
        pass
