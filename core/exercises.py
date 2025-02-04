from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class Exercise:
    name: str
    description: str
    instructions: str
    target_muscles: list[str]
    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_instructions(self) -> str:
        return self.instructions

    def get_target_muscles(self) -> list[str]:
        return self.target_muscles

    def set_target_muscles(self, target_muscles: list[str]) -> None:
        self.target_muscles = target_muscles

    def set_name(self, name: str) -> None:
        self.name = name

    def set_description(self, description: str) -> None:
        self.description = description

    def set_instructions(self, instructions: str) -> None:
        self.instructions = instructions


class ExerciseRepository(Protocol):
    def create(self, exercise: Exercise) -> None:
        pass

    def read_one(self, exercise_id: UUID) -> Exercise:
        pass

    def list(self) -> list[Exercise]:
        pass

    def update(self, exercise_id: UUID, updated_exercise: Exercise) -> None:
        pass

    def delete(self, exercise_id: UUID) -> None:
        pass
