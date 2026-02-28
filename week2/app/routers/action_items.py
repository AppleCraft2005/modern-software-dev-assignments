from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import ActionItemCreate, ActionItemRead


class ExtractRequest(BaseModel):
    text: str
    save_note: Optional[bool] = False


class ExtractItem(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ExtractItem]


class DonePayload(BaseModel):
    done: Optional[bool] = True


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    try:
        if payload.save_note:
            note_id = db.insert_note(text)

        items = extract_action_items(text)
        ids = db.insert_action_items(items, note_id=note_id)
        return ExtractResponse(note_id=note_id, items=[ExtractItem(id=i, text=t) for i, t in zip(ids, items)])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/extract-llm", response_model=ExtractResponse)
async def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    try:
        if payload.save_note:
            note_id = db.insert_note(text)

        items = await extract_action_items_llm(text)
        ids = db.insert_action_items(items, note_id=note_id)
        return ExtractResponse(note_id=note_id, items=[ExtractItem(id=i, text=t) for i, t in zip(ids, items)])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("", response_model=List[ActionItemRead])
def list_all(note_id: Optional[int] = None) -> List[ActionItemRead]:
    rows = db.list_action_items(note_id=note_id)
    return [ActionItemRead(**r) for r in rows]


@router.post("/{action_item_id}/done", response_model=ActionItemRead)
def mark_done(action_item_id: int, payload: DonePayload) -> ActionItemRead:
    done = bool(payload.done)
    try:
        db.mark_action_item_done(action_item_id, done)
        item = db.get_action_item(action_item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="action item not found")
        return ActionItemRead(**item)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


