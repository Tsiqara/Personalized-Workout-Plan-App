from dataclasses import dataclass, field
from datetime import date
from typing import Optional, Protocol
from uuid import UUID, uuid4


@dataclass
class Goal:
    username: str
    goal_type: str  # Example: "Weight", "Exercise"
    target_value: float  # Target weight (kg) or reps/distance for an exercise
    current_value: float  # Tracks progress toward the goal
    exercise_id: Optional[UUID] = None  # Only needed for exercise goals
    target_date: Optional[date] = None  # Deadline to reach the goal
    id: UUID = field(default_factory=uuid4)

    def get_id(self) -> UUID:
        return self.id

    def get_username(self) -> str:
        return self.username

    def get_goal_type(self) -> str:
        return self.goal_type

    def get_target_value(self) -> float:
        return self.target_value

    def get_current_value(self) -> float:
        return self.current_value

    def get_exercise_id(self) -> Optional[UUID]:
        return self.exercise_id

    def get_target_date(self) -> Optional[date]:
        return self.target_date

    def update_progress(self, new_value: float) -> None:
        self.current_value = new_value

    def is_goal_achieved(self) -> bool:
        return self.current_value >= self.target_value

    def set_goal_type(self, new_goal_type: str) -> None:
        self.goal_type = new_goal_type

    def set_target_date(self, new_target_date: date) -> None:
        self.target_date = new_target_date

    def set_target_value(self, new_target_value: float) -> None:
        self.target_value = new_target_value

    def set_exercise_id(self, new_exercise_id: UUID) -> None:
        self.exercise_id = new_exercise_id


class GoalRepository(Protocol):
    def create(self, goal: Goal) -> None:
        pass

    def get(self, goal_id: UUID) -> Goal:
        pass

    def get_by_username(self, username: str) -> list[Goal]:
        pass

    def update(self, goal_id: UUID, new_goal: Goal) -> None:
        pass

    def delete(self, goal_id: UUID) -> None:
        pass
