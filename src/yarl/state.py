from typing import Protocol

import tcod.event
from tcod.console import Console
from tcod.context import Context

import yarl.action


class State(Protocol):
    """Game state protocol based on `tcod.event.EventDispatch`."""

    def handle_events(self, context: Context) -> None: ...
    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None: ...
    def on_render(self, console: Console) -> None: ...
