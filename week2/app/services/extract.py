from __future__ import annotations

import re
from typing import List, Optional
import json

try:
    from ollama import AsyncClient
except Exception:
    AsyncClient = None


BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = ("todo:", "action:", "next:")


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    """Heuristic extractor that returns a list of unique action item strings."""
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line).strip()
            # Trim common checkbox markers
            if cleaned.lower().startswith("[ ]"):
                cleaned = cleaned[3:].strip()
            if cleaned.lower().startswith("[todo]"):
                cleaned = cleaned[6:].strip()
            extracted.append(cleaned)

    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# async def extract_action_items_llm(text: str) -> List[str]:
#     """Use an LLM (if available) to extract action items; fall back to heuristic on error."""
#     if AsyncClient is None:
#         print("DEBUG: AsyncClient tidak tersedia!")
#         return extract_action_items(text)

#     prompt = (
#         "Extract all actionable tasks and action items from the following text. "
#         "Return them as a JSON array of strings. Each task should be a concise, actionable statement.\n\n"
#         f"Text:\n{text}\n\nReturn ONLY a valid JSON array of strings, nothing else."
#     )
#     try:
#         print("DEBUG: Sedang memanggil Ollama...")
#         client = AsyncClient()
#         response = await client.chat(
#             model="llama3.1:8b",
#             messages=[{"role": "user", "content": prompt}],
#             format="json",
#         )
#         response_text = response["message"]["content"]
        
#         print("\n=== JAWABAN MENTAH OLLAMA ===")
#         print(response_text)
#         print("=============================\n")
        
#         action_items = json.loads(response_text)
#         print(f"DEBUG: Tipe data hasil JSON adalah: {type(action_items)}")
        
#         extracted_tasks = []

#         if isinstance(action_items, list):
#             extracted_tasks = [str(i).strip() for i in action_items if str(i).strip()]
#         elif isinstance(action_items, dict):
#             # Jika LLM bandel dan mengembalikan Dictionary
#             for key, value in action_items.items():
#                 if isinstance(value, list):
#                     # Kasus: {"items": ["tugas 1", "tugas 2"]}
#                     extracted_tasks.extend([str(i).strip() for i in value if str(i).strip()])
#                 elif value is None or value == "":
#                     # Kasus: {"tugas 1": null, "tugas 2": null} -> seperti outputmu tadi
#                     extracted_tasks.append(str(key).strip())
#                 elif isinstance(value, str):
#                     # Kasus: {"1": "tugas 1"}
#                     extracted_tasks.append(str(value).strip())
#         if extracted_tasks:
#             print(f"DEBUG: Sukses mengekstrak {len(extracted_tasks)} tugas!")
#             return extracted_tasks
#         else:
#             print("DEBUG: Format salah! Tidak bisa menemukan tugas dari JSON.")
            
#     except Exception as exc:
#         print(f"\n!!! LLM ERROR !!! -> {exc}\n")
#         pass
        
#     print("DEBUG: Gagal pakai LLM, terpaksa Fallback ke fungsi lama (Heuristik).")
#     return extract_action_items(text)


async def extract_action_items_llm(text: str) -> List[str]:
    """Use an LLM (if available) to extract action items; fall back to heuristic on error."""
    if AsyncClient is None:
        return extract_action_items(text)

    prompt = (
        "Extract all actionable tasks and action items from the following text. "
        "Return them as a JSON array of strings. Each task should be a concise, actionable statement.\n\n"
        f"Text:\n{text}\n\nReturn ONLY a valid JSON array of strings, nothing else."
    )
    
    try:
        client = AsyncClient()
        response = await client.chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": prompt}],
            format="json",
        )
        response_text = response["message"]["content"]
        action_items = json.loads(response_text)
        
        extracted_tasks = []

        if isinstance(action_items, list):
            extracted_tasks = [str(i).strip() for i in action_items if str(i).strip()]
        elif isinstance(action_items, dict):
            for key, value in action_items.items():
                if isinstance(value, list):
                    extracted_tasks.extend([str(i).strip() for i in value if str(i).strip()])
                elif value is None or value == "":
                    extracted_tasks.append(str(key).strip())
                elif isinstance(value, str):
                    extracted_tasks.append(str(value).strip())
                    
        if extracted_tasks:
            return extracted_tasks
            
    except Exception:
        pass
        
    return extract_action_items(text)

# async def extract_action_items_llm(text: str) -> List[str]:
#     """Use an LLM (if available) to extract action items; fall back to heuristic on error."""
#     if AsyncClient is None:
#         return extract_action_items(text)

#     prompt = (
#         "Extract all actionable tasks and action items from the following text. "
#         "Return them as a JSON array of strings. Each task should be a concise, actionable statement.\n\n"
#         f"Text:\n{text}\n\nReturn ONLY a valid JSON array of strings, nothing else."
#     )
#     try:
#         client = AsyncClient()
#         response = await client.chat(
#             model="llama3.1:8b",
#             messages=[{"role": "user", "content": prompt}],
#             format="json",
#         )
#         response_text = response["message"]["content"]
#         action_items = json.loads(response_text)
#         if isinstance(action_items, list):
#             return [str(i).strip() for i in action_items if str(i).strip()]
#     except Exception as exc:
#         print(f"LLM ERROR: {exc}")
#         # swallow LLM errors and fall back to heuristic
#         pass
#     return extract_action_items(text)