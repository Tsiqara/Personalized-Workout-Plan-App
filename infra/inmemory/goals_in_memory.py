from dataclasses import dataclass, field
from uuid import UUID

from core.errors import GoalAlreadyExistsError, GoalDoesNotExistError
from core.goals import Goal


@dataclass
class GoalsInMemory:
    goals: dict[UUID, Goal] = field(default_factory=dict)

    def create(self, goal: Goal) -> None:
        if goal.get_id() in self.goals.keys():
            raise GoalAlreadyExistsError(goal.get_id())

        self.goals[goal.get_id()] = goal

    def get(self, goal_id: UUID) -> Goal:
        if goal_id not in self.goals.keys():
            raise GoalDoesNotExistError(goal_id)

        return self.goals[goal_id]

    def get_by_username(self, username: str) -> list[Goal]:
        return [goal for goal in self.goals.values() if goal.get_username() == username]

    def update(self, goal_id: UUID, new_goal: Goal) -> None:
        if goal_id not in self.goals.keys():
            raise GoalDoesNotExistError(goal_id)

        self.goals[goal_id] = new_goal

    def delete(self, goal_id: UUID) -> None:
        del self.goals[goal_id]
