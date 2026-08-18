from typing import Protocol

import yarl.action
import yarl.entity
from yarl.actions import UseItemAction


class Consumable(Protocol):
    parent: yarl.entity.Item

    def get_action(self, consumer: yarl.entity.Actor) -> yarl.action.Action | None: ...
    def activate(self, action: UseItemAction) -> None: ...
