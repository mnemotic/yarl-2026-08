from typing import Protocol

from tcod.console import Console
from tcod.event import Event


class State(Protocol):
    """Game state protocol based on `tcod.event.EventDispatch`."""

    def handle_event(self, event: Event) -> None: ...
    def render(self, console: Console) -> None: ...
