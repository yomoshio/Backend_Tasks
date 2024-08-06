from pydantic import BaseModel, constr
from typing import Optional, List


class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    description: constr(min_length=1)

    class Config:
        from_attributes = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskInDB(TaskBase):
    id: int
    user_id: int


    class Config:
        from_attributes = True


class NoteOut(TaskInDB):
    pass


class TaskPermissionUpdate(BaseModel):
    user_id: int
    can_read: bool = False
    can_update: bool = False
