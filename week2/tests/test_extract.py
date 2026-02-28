import os
import pytest
from unittest.mock import AsyncMock, patch
import json

from week2.app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


@pytest.mark.asyncio
@patch("week2.app.services.extract.chat", new_callable=AsyncMock)
async def test_extract_action_items_llm_with_bulleted_list(mock_chat):
    """Test extract_action_items_llm with a normal bulleted list."""
    text = """
    - Set up database
    - Implement API endpoint
    - Write tests
    """
    
    expected_items = ["Set up database", "Implement API endpoint", "Write tests"]
    mock_chat.return_value = {
        "message": {
            "content": json.dumps(expected_items)
        }
    }
    
    result = await extract_action_items_llm(text)
    
    assert result == expected_items
    mock_chat.assert_called_once()


@pytest.mark.asyncio
@patch("week2.app.services.extract.chat", new_callable=AsyncMock)
async def test_extract_action_items_llm_with_empty_input(mock_chat):
    """Test extract_action_items_llm with an empty input string."""
    text = ""
    
    expected_items = []
    mock_chat.return_value = {
        "message": {
            "content": json.dumps(expected_items)
        }
    }
    
    result = await extract_action_items_llm(text)
    
    assert result == expected_items
    mock_chat.assert_called_once()


@pytest.mark.asyncio
@patch("week2.app.services.extract.chat", new_callable=AsyncMock)
async def test_extract_action_items_llm_with_keyword_prefixes(mock_chat):
    """Test extract_action_items_llm with keyword-prefixed lines."""
    text = """
    todo: Review pull requests
    action: Schedule meeting
    next: Deploy to production
    """
    
    expected_items = ["Review pull requests", "Schedule meeting", "Deploy to production"]
    mock_chat.return_value = {
        "message": {
            "content": json.dumps(expected_items)
        }
    }
    
    result = await extract_action_items_llm(text)
    
    assert result == expected_items
    mock_chat.assert_called_once()


# generate unit tests for the extract_action_items_llm function in extract.py. create using pytest. mock the chat function from ollama so we do not call the LLM during testing. include test cases for: a normal buleted list, an empty input string, and a text with keyword-prefixed lines. ensure the mocked response matches the expected json string format.