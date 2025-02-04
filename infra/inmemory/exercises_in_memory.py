from dataclasses import dataclass, field
from uuid import UUID

from core.errors import ExerciseAlreadyExistsError, ExerciseDoesNotExistError
from core.exercises import Exercise


@dataclass
class ExercisesInMemory:
    exercises: dict[UUID, Exercise] = field(default_factory=dict)

    def create(self, exercise: Exercise) -> None:
        if exercise.get_id() in self.exercises.keys():
            raise ExerciseAlreadyExistsError(exercise.get_id())

        self.exercises[exercise.get_id()] = exercise

    def get(self, exercise_id: UUID) -> Exercise:
        if exercise_id not in self.exercises.keys():
            raise ExerciseDoesNotExistError(exercise_id)

        return self.exercises[exercise_id]

    def list(self) -> list[Exercise]:
        return list(self.exercises.values())

    def update(self, exercise_id: UUID, updated_exercise: Exercise) -> None:
        if exercise_id not in self.exercises.keys():
            raise ExerciseDoesNotExistError(exercise_id)

        self.exercises[exercise_id] = updated_exercise

    def delete(self, exercise_id: UUID) -> None:
        if exercise_id not in self.exercises.keys():
            raise ExerciseDoesNotExistError(exercise_id)

        del self.exercises[exercise_id]
