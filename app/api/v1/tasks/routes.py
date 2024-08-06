from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.tasks.models import Task, Task_Pydantic, TaskPermission_Pydantic, TaskIn_Pydantic, TaskPermission
from app.api.v1.user.models import User_Pydantic, User
from app.api.v1.tasks import logic as l
from app.api.v1.tasks.schemas import TaskCreate, TaskPermissionUpdate
from services.authentication import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=Task_Pydantic,
    summary="Create a Task",
    description="Create a new task with a title and description.",
    response_description="The created task."
)
async def create_new_task(task: TaskCreate, current_user: User_Pydantic = Depends(get_current_user)):
    return await l.create_task_logic(current_user, task.title, task.description)


@router.get(
    "/{task_id}",
    response_model=Task_Pydantic,
    summary="Get a Task",
    description="Retrieve a task by its ID.",
    response_description="The requested task."
)
async def get_task(task_id: int, current_user: User_Pydantic = Depends(get_current_user)):
    task, error = await l.get_task_logic(task_id, current_user)
    if error:
        raise HTTPException(status_code=403 if error == "Permission denied" else 404, detail=error)
    return task


@router.put(
    "/{task_id}",
    response_model=Task_Pydantic,
    summary="Update a Task",
    description="Update the title and description of an existing task.",
    response_description="The updated task."
)
async def update_task(task_id: int, task: TaskCreate, current_user: User_Pydantic = Depends(get_current_user)):
    updated_task = await l.update_task_logic(task_id, task.title, task.description, current_user)
    if not updated_task:
        raise HTTPException(status_code=403, detail="Permission denied")
    return updated_task


@router.delete(
    "/{task_id}",
    summary="Delete a Task",
    description="Delete a task by its ID. Only the owner can delete the task.",
    response_description="Task deletion confirmation."
)
async def delete_task(task_id: int, current_user: User_Pydantic = Depends(get_current_user)):
    result = await l.delete_task_logic(task_id, current_user)
    if not result:
        raise HTTPException(status_code=403, detail="Permission denied")
    return result


@router.post(
    "/{task_id}/permissions",
    response_model=TaskPermission_Pydantic,
    summary="Update Task Permissions",
    description="Update the permissions (read/update) of a task for a specific user. Only the task owner can update permissions.",
    response_description="The updated task permissions."
)
async def update_task_permissions(task_id: int, permission_data: TaskPermissionUpdate,
                                  current_user: User_Pydantic = Depends(get_current_user)):
    permission = await l.update_task_permissions_logic(task_id, permission_data.user_id, permission_data.can_read,
                                                       permission_data.can_update, current_user)
    if not permission:
        raise HTTPException(status_code=403, detail="Permission denied")
    return permission
