from backend.app.services.extract import (
    _detect_due_date,
    _detect_priority,
    extract_action_items,
)


def test_extract_action_items_basic():
    """Original action items are still detected (backward compat)."""
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    descriptions = [i["description"] for i in items]
    assert "TODO: write tests" in descriptions
    assert "ACTION: review PR" in descriptions
    assert "Ship it!" in descriptions


def test_extract_returns_dicts_with_expected_keys():
    items = extract_action_items("TODO: something")
    assert len(items) == 1
    item = items[0]
    assert set(item.keys()) == {"description", "priority", "due_date"}


# ---- Priority detection ----

def test_priority_high_keywords():
    for word in ("ASAP", "urgent", "critical", "immediately", "important"):
        assert _detect_priority(f"Fix the build {word}") == "High"


def test_priority_low_keywords():
    for word in ("eventually", "someday", "low priority", "when possible", "no rush"):
        assert _detect_priority(f"Clean up code {word}") == "Low"


def test_priority_defaults_to_medium():
    assert _detect_priority("TODO: write docs") == "Medium"


def test_extract_assigns_priority():
    text = "TODO: fix bug ASAP\nTODO: refactor someday\nTODO: write docs"
    items = extract_action_items(text)
    assert items[0]["priority"] == "High"
    assert items[1]["priority"] == "Low"
    assert items[2]["priority"] == "Medium"


# ---- Due date detection ----

def test_due_date_iso():
    assert _detect_due_date("Submit report by 2026-03-15") == "2026-03-15"


def test_due_date_slash():
    assert _detect_due_date("Finish task due 3/15/2026") == "3/15/2026"


def test_due_date_month_name():
    assert _detect_due_date("Send invoice by March 15") == "March 15"
    assert _detect_due_date("Send invoice by Jan 2, 2026") == "Jan 2, 2026"


def test_due_date_relative():
    assert _detect_due_date("Review PR by tomorrow") == "tomorrow"
    assert _detect_due_date("Deploy due next week") == "next week"


def test_due_date_none():
    assert _detect_due_date("Just a normal sentence") is None


def test_extract_assigns_due_date():
    text = "TODO: submit report by 2026-03-15\nTODO: write docs"
    items = extract_action_items(text)
    assert items[0]["due_date"] == "2026-03-15"
    assert items[1]["due_date"] is None


# ---- New prefix detection ----

def test_extract_task_and_fix_prefixes():
    text = "TASK: deploy service\nFIX: memory leak"
    items = extract_action_items(text)
    assert len(items) == 2


def test_extract_follow_up_prefix():
    text = "Follow up: check with team\nFollow-up: send email"
    items = extract_action_items(text)
    assert len(items) == 2


# ---- Lines with due dates are auto-detected as action items ----

def test_line_with_due_date_extracted():
    text = "Complete review by 2026-04-01"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0]["due_date"] == "2026-04-01"


# ---- Lines with urgent keywords are auto-detected ----

def test_line_with_urgent_keyword_extracted():
    text = "Server is down, this is critical"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0]["priority"] == "High"

