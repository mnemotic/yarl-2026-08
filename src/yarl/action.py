from typing import Protocol


class Action(Protocol):
    """Action protocol."""

    def perform(self) -> None:
        """Perform this action."""
