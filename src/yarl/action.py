from typing import Protocol

import yarl.engine
import yarl.entity


class Action(Protocol):
    """Action protocol."""

    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        """Perform this action."""
