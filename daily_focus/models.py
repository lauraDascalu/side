from sqlmodel import SQLModel, Field
from datetime import datetime

class TaskLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    seconds: int
    created_at: datetime = Field(default_factory=datetime.now)
    date_str: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

class ActiveTimer(SQLModel, table=True):
    task_name: str = Field(primary_key=True)
    start_time: float

class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    is_completed: bool = Field(default=False)