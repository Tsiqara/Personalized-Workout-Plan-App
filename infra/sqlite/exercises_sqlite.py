from dataclasses import dataclass
from uuid import UUID

from core.errors import ExerciseAlreadyExistsError
from core.exercises import Exercise
from infra.sqlite.database_sqlite import SqliteDatabase


@dataclass
class ExercisesSqlite:
    sqlite_database: SqliteDatabase

    def create(self, exercise: Exercise) -> None:
        self._check_exists(exercise.get_id())

        exercise_id = exercise.get_id()
        name = exercise.get_name()
        description = exercise.get_description()
        instructions = exercise.get_instructions()
        target_muscles = ", ".join(exercise.get_target_muscles())

        query2 = (
            "INSERT INTO main.exercises (id, name, description, instructions, target_muscles) "
            "VALUES (?, ?, ?, ?, ?);"
        )
        params2 = (
            exercise_id,
            name,
            description,
            instructions,
            target_muscles,
        )

        self.sqlite_database.execute(query2, params2)

    def _check_exists(self, exercise_id: UUID) -> None:
        query = "SELECT ID FROM exercises WHERE ID = ?"
        params = (exercise_id,)
        result = self.sqlite_database.fetch_one(query, params)
        if result is not None:
            raise ExerciseAlreadyExistsError(exercise_id)

    def get(self, exercise_id: UUID) -> Exercise:
        self._check_exists(exercise_id)

        query = "SELECT * FROM exercises WHERE ID = ?"
        params = (exercise_id,)

        result = self.sqlite_database.fetch_one(query, params)

        target_muscles = result[4].split(", ")

        return Exercise(
            name=result[1],
            description=result[2],
            instructions=result[3],
            target_muscles=target_muscles,
            id=UUID(result[0]),
        )

    def list(self) -> list[Exercise]:
        query = "SELECT * FROM exercises"
        result = list(self.sqlite_database.fetch_all(query))

        return [
            Exercise(
                res[1],
                res[2],
                res[3],
                res[4].split(", "),
                UUID(res[0]),
            )
            for res in result
        ]

    def update(self, exercise_id: UUID, updated_exercise: Exercise) -> None:
        self._check_exists(exercise_id)

        if exercise_id != updated_exercise.get_id():
            raise ValueError("Tried to update incorrect exercise")

        query = "UPDATE exercises SET name = ?, description = ?, instructions = ?, target_muscles = ? WHERE ID = ?"
        params = (
            updated_exercise.name,
            updated_exercise.description,
            updated_exercise.instructions,
            ", ".join(updated_exercise.target_muscles),
            exercise_id,
        )

        self.sqlite_database.execute(query, params)

    def delete(self, exercise_id: UUID) -> None:
        self._check_exists(exercise_id)

        query = "DELETE FROM exercises WHERE ID = ?"
        params = (exercise_id,)
        self.sqlite_database.execute(query, params)
