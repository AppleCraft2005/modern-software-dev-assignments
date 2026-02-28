from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteRead


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate) -> NoteRead:
    try:
        note_id = db.insert_note(payload.content)
        note = db.get_note(note_id)
        if note is None:
            raise HTTPException(status_code=500, detail="failed to retrieve created note")
        return NoteRead(**note)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{note_id}", response_model=NoteRead)
def get_single_note(note_id: int) -> NoteRead:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteRead(**row)


@router.get("/", response_model=List[NoteRead])
def list_notes() -> List[NoteRead]:
    rows = db.list_notes()
    return [NoteRead(**r) for r in rows]


