from fastapi import FastAPI

from app_auth.base_config import auth_backend, fastapi_users
from app_auth.schemas import UserRead, UserCreate
from tasks.router import tasks_router, create_task_router


app = FastAPI(
    title="ToDo"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(tasks_router)
app.include_router(create_task_router)