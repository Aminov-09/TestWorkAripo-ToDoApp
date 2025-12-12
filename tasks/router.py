from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from typing import List
from datetime import datetime

from db.database import get_async_session
from tasks.models import Task, StatusEnum
from tasks.schemas import TaskRead, TaskCreate
from app_auth.models import User
from app_auth.base_config import current_user
router = APIRouter()

# ========================
# Роутер для списка заказов
# ========================
tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])


@tasks_router.get("/", response_model=List[TaskRead])
async def get_tasks(
        status: StatusEnum | None = Query(
            None,
            description=f"Фильтровать по статусу. Возможные значения: {[s.value for s in StatusEnum]}"
        ),
        sort: str = Query(
            "desc",
            regex="^(asc|desc)$",
            description="Сортировать по возрастанию - 'asc', по убыванию - 'desc'"
        ),
        current_user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session),
):
    query = select(Task)

    if status:
        query = query.where(Task.status == status)

    # Сортировка по дате создания
    if sort == "asc":
        query = query.order_by(asc(Task.created_at))
    else:
        query = query.order_by(desc(Task.created_at))

    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks



# ========================
# Роутер для создания заказа
# ========================
create_task_router = APIRouter(prefix="/create_task", tags=["create_task"])


@create_task_router.post("/", response_model=TaskRead)
async def create_task(
        task: TaskCreate,
        current_user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session)
):
    new_task = Task(**task.dict(), user_id=current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# ========================
# Роутер для удаления заказа (только владелец)
# ========================
@tasks_router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user: User = Depends(current_user),
        db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Order not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can delete only your own orders")

    await db.delete(task)
    await db.commit()
    return {"detail": "Order deleted"}
