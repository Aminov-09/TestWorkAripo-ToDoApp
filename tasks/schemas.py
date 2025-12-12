from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from tasks.models import StatusEnum


# Схема для чтения задачи
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: StatusEnum
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True  # важно для SQLAlchemy


# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.TODO
