from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True
