from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr


NonEmptyStr = constr(min_length=1)


class NoteCreate(BaseModel):
    content: NonEmptyStr = Field(..., description="Note content")


class NoteRead(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemCreate(BaseModel):
    text: NonEmptyStr = Field(..., description="Action item text")
    note_id: Optional[int] = Field(None, description="Optional parent note id")


class ActionItemRead(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str
