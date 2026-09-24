from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class ItemType(StrEnum):
    TODO = "todo"
    TASK = "task"
    REMINDER = "reminder"
    EVENT = "event"


class BaseItem(BaseModel):
    title: str
    description: str = ""


class Todo(BaseItem):
    type: Literal[ItemType.TODO] = ItemType.TODO

    completed: bool = False


class Task(BaseItem):
    type: Literal[ItemType.TASK] = ItemType.TASK

    due_at: datetime | None = None
    priority: int | None = Field(default=None, ge=1, le=5)


class Reminder(BaseItem):
    type: Literal[ItemType.REMINDER] = ItemType.REMINDER

    remind_at: datetime | None = None
    recurrence: str | None = None


class Event(BaseItem):
    type: Literal[ItemType.EVENT] = ItemType.EVENT

    start_at: datetime
    end_at: datetime | None = None
    location: str | None = None
    attendees: list[str] = Field(default_factory=list)


ExtractedItem = Annotated[
    Todo|Task|Reminder|Event|None,
    Field(discriminator="type"),
]
