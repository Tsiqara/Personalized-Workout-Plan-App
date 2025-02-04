from dataclasses import dataclass
from uuid import UUID

from core.errors import GoalAlreadyExistsError
from core.goals import Goal
from infra.sqlite.database_sqlite import SqliteDatabase


@dataclass
class GoalsSqlite:
    sqlite_database: SqliteDatabase

    def create(self, goal: Goal) -> None:
        self._check_exists(goal.get_id())

        goal_id = goal.get_id()
        username = goal.get_username()
        goal_type = goal.get_goal_type()
        target_value = goal.get_target_value()
        current_value = goal.get_current_value()
        exercise_id = goal.get_exercise_id()
        target_date = goal.get_target_date()

        query = (
            "INSERT INTO goals (ID, username, goal_type, target_value, current_value, exercise_id, target_date)"
            "VALUES (?, ?, ?, ?, ?, ?, ?);"
        )
        params = (
            goal_id,
            username,
            goal_type,
            target_value,
            current_value,
            exercise_id,
            target_date,
        )

        self.sqlite_database.execute(query, params)

    def get(self, goal_id: UUID) -> Goal:
        self._check_exists(goal_id)

        query = "SELECT username, goal_type, target_value, current_value, exercise_id, target_date FROM goals WHERE ID = ?"
        params = (goal_id,)

        result = self.sqlite_database.fetch_one(query, params)

        username = result[0]
        goal_type = result[1]
        target_value = result[2]
        current_value = result[3]
        exercise_id = result[4]
        target_date = result[5]

        return Goal(
            id=goal_id,
            username=username,
            goal_type=goal_type,
            target_value=target_value,
            current_value=current_value,
            exercise_id=exercise_id,
            target_date=target_date,
        )

    def get_by_username(self, username: str) -> list[Goal]:
        query = "SELECT ID FROM goals WHERE username = ?"
        params = (username,)

        result = self.sqlite_database.fetch_all(query, params)

        return [self.get(r[0]) for r in result]

    def update(self, goal_id: UUID, new_goal: Goal) -> None:
        self._check_exists(goal_id)

        if new_goal.get_id() != goal_id:
            raise ValueError("Changing incorrect goal")

        username = new_goal.get_username()
        goal_type = new_goal.get_goal_type()
        target_value = new_goal.get_target_value()
        current_value = new_goal.get_current_value()
        exercise_id = new_goal.get_exercise_id()
        target_date = new_goal.get_target_date()

        query = (
            "UPDATE main.goals SET username = ?, goal_type = ?, target_value = ?, current_value = ?, exercise_id "
            "= ?, target_date = ? WHERE ID = ?"
        )
        params = (
            goal_id,
            username,
            goal_type,
            target_value,
            current_value,
            exercise_id,
            target_date,
        )

        self.sqlite_database.execute(query, params)

    def delete(self, goal_id: UUID) -> None:
        self._check_exists(goal_id)

        query = "DELETE FROM goals WHERE ID = ?"
        params = (goal_id,)
        self.sqlite_database.execute(query, params)

    def _check_exists(self, goal_id: UUID) -> None:
        query = "SELECT ID FROM goals WHERE ID = ?"
        params = (goal_id,)
        result = self.sqlite_database.fetch_one(query, params)

        if result is not None:
            raise GoalAlreadyExistsError(goal_id)
