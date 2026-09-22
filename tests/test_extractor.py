import pytest
from item_extractor import Event, Reminder, Task, Todo, extract


def test_extract_todo():
    items = extract("Organize the garage")
    assert len(items) >= 1
    assert isinstance(items[0], Todo)

def test_extract_task():
    items = extract("Finish the Q3 financial report before 5 PM")
    assert len(items) >= 1
    assert isinstance(items[0], Task)

def test_extract_event():
    items = extract("Doctor appointment on Monday at 10:30 AM")
    assert len(items) >= 1
    assert isinstance(items[0], Event)

def test_extract_reminder():
    items = extract("Remind me to grab milk when I leave work")
    assert len(items) >= 1
    assert isinstance(items[0], Reminder)
