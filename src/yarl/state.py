from typing import Protocol

import tcod.event

import yarl.action


class State(Protocol):
    """Game state protocol based on `tcod.event.EventDispatch`."""

    def handle_events(self) -> None: ...
    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None:
        """Called on events."""
