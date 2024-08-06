from app.api.v1.tasks.models import Task, TaskPermission
from app.api.v1.user.models import User


async def create_task_logic(owner: User, title: str, description: str):
    task = await Task.create(title=title, description=description, owner=owner)
    return task


async def get_task_logic(task_id: int, user: User):
    task = await Task.filter(id=task_id).first()
    if not task:
        return None, "Task not found"
    if task.owner_id != user.id and not await TaskPermission.filter(task=task, user=user, can_read=True).exists():
        return None, "Permission denied"
    return task, None


async def update_task_logic(task_id: int, title: str, description: str, user: User):
    task = await Task.get(id=task_id)
    if task.owner_id != user.id:
        return None, "Permission denied"
    task.title = title
    task.description = description
    await task.save()
    return task


async def delete_task_logic(task_id: int, user: User):
    task = await Task.get(id=task_id)
    if task.owner_id != user.id:
        return None, "Permission denied"
    await task.delete()
    return {"detail": "Task deleted"}


async def update_task_permissions_logic(task_id: int, user_id: int, can_read: bool, can_update: bool,
                                        current_user: User):
    task = await Task.get(id=task_id)
    if task.owner_id != current_user.id:
        return None, "Only task owner can update permissions"
    user = await User.get(id=user_id)
    permission, created = await TaskPermission.get_or_create(task=task, user=user)
    permission.can_read = can_read
    permission.can_update = can_update
    await permission.save()
    return permission
