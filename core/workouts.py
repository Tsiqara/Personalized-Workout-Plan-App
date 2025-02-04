from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Union
from uuid import UUID, uuid4

from core.exercises import Exercise
from core.goals import Goal


@dataclass
class Workout:
    username: str
    frequency_per_week: int
    goals: list[Goal]
    daily_duration_minutes: int
    exercises: dict[
        UUID, dict[str, Union[int, float]]
    ]  # Exercise ID -> repetitions, sets, duration/distance.
    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_username(self) -> str:
        return self.username

    def get_frequency(self) -> int:
        return self.frequency_per_week

    def get_goals(self) -> list[Goal]:
        return self.goals

    def get_daily_duration(self) -> int:
        return self.daily_duration_minutes

    def get_exercises(self) -> dict[UUID, dict[str, Union[int, float]]]:
        return self.exercises

    def set_frequency(self, frequency: int) -> None:
        self.frequency_per_week = frequency

    def set_goals(self, goals: list[Goal]) -> None:
        self.goals = goals

    def add_goal(self, goal: Goal) -> None:
        self.goals.append(goal)

    def remove_goal(self, goal: Goal) -> None:
        self.goals.remove(goal)

    def set_daily_duration(self, daily_duration: int) -> None:
        self.daily_duration_minutes = daily_duration

    def set_exercises(
        self, exercises: dict[UUID, dict[str, Union[int, float]]]
    ) -> None:
        self.exercises = exercises

    def add_exercise(
        self,
        exercise: Exercise,
        repetitions: int = 0,
        sets: int = 0,
        duration: float = 0,
        distance: float = 0,
    ) -> None:
        self.exercises[exercise.get_id()] = {
            "repetitions": repetitions,
            "sets": sets,
            "duration": duration,
            "distance": distance,
        }

    def remove_exercise(self, exercise_id: UUID) -> None:
        del self.exercises[exercise_id]


class WorkoutRepository(Protocol):
    def create(self, workout: Workout) -> None:
        pass

    def get(self, workout_id: UUID) -> Workout:
        pass

    def get_by_username(self, username: str) -> list[Workout]:
        pass

    def update(self, workout_id: UUID, workout: Workout) -> None:
        pass

    def delete(self, workout_id: UUID) -> None:
        pass
