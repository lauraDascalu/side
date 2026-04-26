from sqlmodel import SQLModel, Field
from datetime import datetime

class TaskLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    seconds: int
    created_at: datetime = Field(default_factory=datetime.now)
    date_str: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))