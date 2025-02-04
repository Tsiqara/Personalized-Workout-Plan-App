from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from core.exercises import ExerciseRepository
from core.goals import GoalRepository
from core.users import UserRepository
from core.weight_records import WeightRecordRepository
from core.workouts import WorkoutRepository
from infra.inmemory.blacklist_tokens import BlacklistTokensInMemory


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.users  # type: ignore


def get_exercise_repository(request: Request) -> ExerciseRepository:
    return request.app.state.exercises  # type: ignore


def get_workout_repository(request: Request) -> WorkoutRepository:
    return request.app.state.workouts  # type: ignore


def get_goal_repository(
        request: Request,
) -> GoalRepository:
    return request.app.state.goals  # type: ignore


def get_weight_record_repository(
        request: Request,
) -> WeightRecordRepository:
    return request.app.state.weights  # type: ignore


def get_blacklist_repository(
        request: Request,
) -> BlacklistTokensInMemory:
    return request.app.state.blacklist  # type: ignore


UserRepositoryDependable = Annotated[UserRepository, Depends(get_user_repository)]
ExerciseRepositoryDependable = Annotated[ExerciseRepository, Depends(get_exercise_repository)]
WorkoutRepositoryDependable = Annotated[WorkoutRepository, Depends(get_workout_repository)]
GoalRepositoryDependable = Annotated[GoalRepository, Depends(get_goal_repository)]
WeightRecordRepositoryDependable = Annotated[WeightRecordRepository, Depends(get_weight_record_repository)]
BlacklistedUserRepositoryDependable = Annotated[BlacklistTokensInMemory, Depends(get_blacklist_repository)]
