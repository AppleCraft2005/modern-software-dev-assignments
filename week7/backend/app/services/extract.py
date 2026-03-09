import re
from typing import Optional

# Priority keyword mappings (checked against lowercased text)
_HIGH_KEYWORDS = re.compile(
    r"\b(asap|urgent|urgently|critical|critically|immediately|important|high priority)\b",
    re.IGNORECASE,
)
_LOW_KEYWORDS = re.compile(
    r"\b(eventually|someday|low priority|when possible|no rush|nice to have)\b",
    re.IGNORECASE,
)

# Due-date patterns
_DATE_ISO = re.compile(
    r"(?:by|due|before|deadline)\s+(\d{4}-\d{2}-\d{2})", re.IGNORECASE
)
_DATE_SLASH = re.compile(
    r"(?:by|due|before|deadline)\s+(\d{1,2}/\d{1,2}/\d{4})", re.IGNORECASE
)
_DATE_MONTH_NAME = re.compile(
    r"(?:by|due|before|deadline)\s+"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}(?:,?\s*\d{4})?)",
    re.IGNORECASE,
)
_DATE_RELATIVE = re.compile(
    r"(?:by|due|before|deadline)\s+(tomorrow|next (?:week|monday|tuesday|wednesday|thursday|friday))",
    re.IGNORECASE,
)


def _detect_priority(text: str) -> str:
    """Return 'High', 'Medium', or 'Low' based on keyword analysis."""
    if _HIGH_KEYWORDS.search(text):
        return "High"
    if _LOW_KEYWORDS.search(text):
        return "Low"
    return "Medium"


def _detect_due_date(text: str) -> Optional[str]:
    """Extract a due-date string from the text, or return None."""
    for pattern in (_DATE_ISO, _DATE_SLASH, _DATE_MONTH_NAME, _DATE_RELATIVE):
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return None


def _is_action_item(line: str) -> bool:
    """Determine whether a line qualifies as an action item."""
    normalized = line.lower()
    # Explicit prefixes
    if normalized.startswith(("todo:", "action:", "task:", "fix:", "follow up:", "follow-up:")):
        return True
    # Ends with exclamation mark (imperative)
    if line.endswith("!"):
        return True
    # Contains a due-date reference
    if _detect_due_date(line) is not None:
        return True
    # Contains high-priority keywords
    if _HIGH_KEYWORDS.search(line):
        return True
    return False


def extract_action_items(text: str) -> list[dict]:
    """Extract action items from *text* with priority and optional due date.

    Returns a list of dicts, each with keys:
        - description (str)
        - priority    ('High' | 'Medium' | 'Low')
        - due_date    (str | None)
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[dict] = []
    for line in lines:
        if _is_action_item(line):
            results.append(
                {
                    "description": line,
                    "priority": _detect_priority(line),
                    "due_date": _detect_due_date(line),
                }
            )
    return results

