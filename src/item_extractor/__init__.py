from .extractor import Extractor
from .models import (
    Event,
    ExtractedItem,
    ItemType,
    Reminder,
    Task,
    Todo,
)

# Create a default instance on module load
_default_extractor = Extractor()


def extract(text: str) -> list[ExtractedItem]:
    return _default_extractor.extract(text)


__all__ = [
    "extract",
    "Extractor",
    "ExtractedItem",
    "ItemType",
    "Todo",
    "Task",
    "Reminder",
    "Event",
]
