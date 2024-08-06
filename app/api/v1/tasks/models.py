from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Task(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    owner = fields.ForeignKeyField('models.User', related_name='tasks')
    assignees = fields.ManyToManyField('models.User', related_name='assigned_tasks', through='task_permissions')


class TaskPermission(models.Model):
    task = fields.ForeignKeyField('models.Task', related_name='permissions')
    user = fields.ForeignKeyField('models.User', related_name='permissions')
    can_read = fields.BooleanField(default=False)
    can_update = fields.BooleanField(default=False)


Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)
TaskPermission_Pydantic = pydantic_model_creator(TaskPermission, name="TaskPermission")