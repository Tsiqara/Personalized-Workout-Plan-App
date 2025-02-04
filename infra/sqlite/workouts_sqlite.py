import uuid
from dataclasses import dataclass
from uuid import UUID

from core.errors import WorkoutAlreadyExistsError, WorkoutDoesNotExistError
from core.workouts import Workout
from infra.sqlite.database_sqlite import SqliteDatabase


@dataclass
class WorkoutsSqlite:
    sqlite_database: SqliteDatabase

    def create(self, workout: Workout) -> None:
        query = "SELECT ID FROM workouts WHERE ID = ?"
        params = (workout.get_id(),)

        result = self.sqlite_database.fetch_one(query, params)

        if result is not None:
            raise WorkoutAlreadyExistsError(workout.get_id())

        workout_id = workout.get_id()
        username = workout.get_username()
        frequency = workout.get_frequency()
        daily_duration = workout.get_daily_duration()

        query2 = (
            "INSERT INTO workouts (ID, username, frequency_per_week, daily_duration_minutes)"
            "VALUES (?, ?, ?, ?);"
        )
        params2 = (
            workout_id,
            username,
            frequency,
            daily_duration,
        )

        self.sqlite_database.execute(query2, params2)

        for exercise_id, details in workout.get_exercises():
            repetitions = details["repetitions"]
            sets = details["sets"]
            duration = details["duration"]
            distance = details["distance"]

            query2 = (
                "INSERT INTO workout_exercises (WORKOUT_ID, EXERCISE_ID, REPETITIONS, SET_NUMBER, DURATION, DISTANCE)"
                "VALUES (?, ?, ?, ?, ?, ?);"
            )
            params2 = (
                workout_id,
                exercise_id,
                repetitions,
                sets,
                duration,
                distance,
            )

            self.sqlite_database.execute(query2, params2)

        for goal_id in workout.get_goals():
            query2 = (
                "INSERT INTO main.workout_goals (workout_ID, goal_ID)" "VALUES (?, ?);"
            )
            params2 = (
                workout_id,
                goal_id,
            )

            self.sqlite_database.execute(query2, params2)

    def get(self, workout_id: UUID) -> Workout:
        query = "SELECT * FROM workouts WHERE ID = ?"
        params = (workout_id,)

        result = self.sqlite_database.fetch_one(query, params)
        if result is None:
            raise WorkoutDoesNotExistError(workout_id)

        workout_id = UUID(result[0])
        username = result[1]
        frequency = result[2]
        daily_duration = result[3]

        query = "SELECT goal_ID FROM workout_goals WHERE workout_ID = ?"
        params = (workout_id,)

        goals = [
            uuid.UUID(goal_id[0])
            for goal_id in list(self.sqlite_database.fetch_all(query, params))
        ]

        query = (
            "SELECT exercise_ID, repetitions, set_number, duration, distance FROM workout_exercises WHERE "
            "workout_ID = ?"
        )
        params = (workout_id,)

        result = list(self.sqlite_database.fetch_all(query, params))

        exercises = {}
        for r in result:
            exercises[r[0]] = {
                "repetitions": r[1],
                "sets": r[2],
                "duration": r[3],
                "distance": r[4],
            }

        return Workout(
            username=username,
            frequency_per_week=frequency,
            goals=goals,
            daily_duration_minutes=daily_duration,
            exercises=exercises,
            id=workout_id,
        )

    def get_by_username(self, username: str) -> list[Workout]:
        query = "SELECT ID FROM workouts WHERE username = ?"
        params = (username,)

        result = self.sqlite_database.fetch_all(query, params)

        workouts = []
        for r in result:
            workout_id = r[0]
            workouts.append(self.get(workout_id))

        return workouts

    def update(self, workout_id: UUID, workout: Workout) -> None:
        query = "SELECT ID FROM workouts WHERE ID = ?"
        params = (workout.get_id(),)

        result = self.sqlite_database.fetch_one(query, params)

        if result is None:
            raise WorkoutDoesNotExistError(workout.get_id())

        workout_id = workout.get_id()
        username = workout.get_username()
        frequency = workout.get_frequency()
        daily_duration = workout.get_daily_duration()

        query2 = "UPDATE workouts SET username = ?, frequency_per_week = ?, daily_duration_minutes = ? WHERE ID = ?"
        params2 = (
            username,
            frequency,
            daily_duration,
            workout_id,
        )

        self.sqlite_database.execute(query2, params2)

        query2 = "DELETE FROM workout_exercises WHERE workout_id = ?;"
        params2 = (workout_id,)

        self.sqlite_database.execute(query2, params2)

        for exercise_id, details in workout.get_exercises():
            repetitions = details["repetitions"]
            sets = details["sets"]
            duration = details["duration"]
            distance = details["distance"]

            query2 = (
                "INSERT INTO workout_exercises (WORKOUT_ID, EXERCISE_ID, REPETITIONS, SET_NUMBER, DURATION, DISTANCE)"
                "VALUES (?, ?, ?, ?, ?, ?);"
            )
            params2 = (
                workout_id,
                exercise_id,
                repetitions,
                sets,
                duration,
                distance,
            )

            self.sqlite_database.execute(query2, params2)

        query2 = "DELETE FROM workout_goals WHERE workout_id = ?;"
        params2 = (workout_id,)

        self.sqlite_database.execute(query2, params2)

        for goal_id in workout.get_goals():
            query2 = (
                "INSERT INTO main.workout_goals (workout_ID, goal_ID)" "VALUES (?, ?);"
            )
            params2 = (
                workout_id,
                goal_id,
            )

            self.sqlite_database.execute(query2, params2)

    def delete(self, workout_id: UUID) -> None:
        query2 = "DELETE FROM workout_exercises WHERE workout_id = ?;"
        params2 = (workout_id,)

        self.sqlite_database.execute(query2, params2)

        query2 = "DELETE FROM workout_goals WHERE workout_id = ?;"
        params2 = (workout_id,)

        self.sqlite_database.execute(query2, params2)

        query2 = "DELETE FROM workouts WHERE ID = ?;"
        params2 = (workout_id,)

        self.sqlite_database.execute(query2, params2)
