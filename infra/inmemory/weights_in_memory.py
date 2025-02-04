from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from core.errors import WeightRecordAlreadyExistsError
from core.weight_records import WeightRecord


@dataclass
class WeightsInMemory:
    weights: dict[UUID, WeightRecord] = field(default_factory=dict)

    def create(self, weight_record: WeightRecord) -> None:
        if weight_record.get_id() in self.weights.keys():
            raise WeightRecordAlreadyExistsError(weight_record.get_id())

    def get_by_user_id(self, username: str) -> list[WeightRecord]:
        return [
            record
            for record in self.weights.values()
            if record.get_username() == username
        ]

    def get_latest(self, username: str) -> WeightRecord | None:
        user_records = self.get_by_user_id(username)

        latest_record = max(user_records, key=lambda record: record.get_date())
        return latest_record

    def delete(self, record_id: UUID) -> None:
        del self.weights[record_id]
