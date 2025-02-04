import os

from fastapi import FastAPI

from constants import DB_PATH
from infra.fastapi.users import user_api
from infra.inmemory.exercises_in_memory import ExercisesInMemory
from infra.inmemory.goals_in_memory import GoalsInMemory
from infra.inmemory.users_in_memory import UsersInMemory
from infra.inmemory.weights_in_memory import WeightsInMemory
from infra.inmemory.workouts_in_memory import WorkoutsInMemory
from infra.sqlite.database_sqlite import SqliteDatabase
from infra.sqlite.exercises_sqlite import ExercisesSqlite
from infra.sqlite.goals_sqlite import GoalsSqlite
from infra.sqlite.users_sqlite import UsersSqlite
from infra.sqlite.weights_sqlite import WeightsSqlite
from infra.sqlite.workouts_sqlite import WorkoutsSqlite


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    # app.include_router(wallet_api)
    # app.include_router(transaction_api)
    # app.include_router(statistic_api)

    # comment line below when you are using test-mode
    # os.environ["REPOSITORY_KIND"] = "sqlite"

    if os.getenv("REPOSITORY_KIND", "memory") == "sqlite":
        sqlite_database = SqliteDatabase(DB_PATH)
        app.state.users = UsersSqlite(sqlite_database)
        app.state.exercises = ExercisesSqlite(sqlite_database)
        app.state.workouts = WorkoutsSqlite(sqlite_database)
        app.state.goals = GoalsSqlite(sqlite_database)
        app.state.weights = WeightsSqlite(sqlite_database)
    else:
        app.state.users = UsersInMemory()
        app.state.exercises = ExercisesInMemory()
        app.state.workouts = WorkoutsInMemory()
        app.state.goals = GoalsInMemory()
        app.state.weights = WeightsInMemory()

    return app
