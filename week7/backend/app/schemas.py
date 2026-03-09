from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1, max_length=10000)
    category_id: int | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    category_id: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None


class ActionItemCreate(BaseModel):
    description: str
    priority: str = "Medium"
    due_date: str | None = None


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    priority: str
    due_date: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None
    priority: str | None = None
    due_date: str | None = None


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class CategoryRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000)


class ExtractedItem(BaseModel):
    description: str
    priority: str
    due_date: str | None = None


