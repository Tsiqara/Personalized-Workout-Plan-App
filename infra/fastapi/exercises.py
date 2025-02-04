from uuid import UUID

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from core.errors import ExerciseAlreadyExistsError
from core.exercises import Exercise
from core.users import User
from infra.fastapi.dependables import ExerciseRepositoryDependable, UserRepositoryDependable, \
    BlacklistedUserRepositoryDependable
from infra.fastapi.users import get_current_user

exercise_api = APIRouter(tags=["Exercises"])


class ExerciseCreateRequest(BaseModel):
    name: str
    description: str
    instructions: str
    target_muscles: list[str]


class ExerciseCreateResponse(BaseModel):
    exercise: Exercise


@exercise_api.post("/exercises", response_model=ExerciseCreateResponse)
def create_exercise(request: ExerciseCreateRequest, exercises: ExerciseRepositoryDependable,
                    users: UserRepositoryDependable, blacklist: BlacklistedUserRepositoryDependable, token: str = Header(alias="token")):
    get_current_user(users, blacklist, token)
    new_exercise = Exercise(request.name, request.description, request.instructions, request.target_muscles)
    exercises.create(new_exercise)
    return new_exercise
