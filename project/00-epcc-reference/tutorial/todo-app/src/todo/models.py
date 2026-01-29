"""Data models for the todo application."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class TodoItem:
    """A single todo item.

    Attributes:
        id: Unique identifier (8-character hex string)
        title: Description of the todo item
        completed: Whether the item is done
        created_at: When the item was created
        completed_at: When the item was completed (None if not completed)
    """

    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def complete(self) -> None:
        """Mark this todo item as completed."""
        self.completed = True
        self.completed_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the todo item.
        """
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TodoItem":
        """Create a TodoItem from a dictionary.

        Args:
            data: Dictionary with todo item data.

        Returns:
            A new TodoItem instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data["completed_at"]
                else None
            ),
        )
