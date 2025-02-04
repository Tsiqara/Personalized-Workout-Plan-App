from dataclasses import dataclass, field
from uuid import UUID

from core.errors import WorkoutAlreadyExistsError, WorkoutDoesNotExistError
from core.workouts import Workout


@dataclass
class WorkoutsInMemory:
    workouts: dict[UUID, Workout] = field(default_factory=dict)

    def create(self, workout: Workout) -> None:
        if workout.get_id() in self.workouts.keys():
            raise WorkoutAlreadyExistsError(workout.get_id())

        self.workouts[workout.get_id()] = workout

    def get(self, workout_id: UUID) -> Workout:
        if workout_id not in self.workouts.keys():
            raise WorkoutDoesNotExistError(workout_id)

        return self.workouts[workout_id]

    def get_by_username(self, username: str) -> list[Workout]:
        return [
            workout
            for workout in self.workouts.values()
            if workout.get_username() == username
        ]

    def update(self, workout_id: UUID, workout: Workout) -> None:
        if workout_id not in self.workouts.keys():
            raise WorkoutDoesNotExistError(workout_id)

        self.workouts[workout_id] = workout

    def delete(self, workout_id: UUID) -> None:
        del self.workouts[workout_id]
