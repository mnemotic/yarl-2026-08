from abc import abstractmethod

import yarl.actions
from yarl import colors
from yarl.action import Action
from yarl.components.base_component import BaseComponent
from yarl.entity import Actor, Item
from yarl.exceptions import ImpossibleActionError


class BaseConsumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Action | None:
        return yarl.actions.UseItemAction(consumer, self.parent)

    @abstractmethod
    def activate(self, action: yarl.actions.UseItemAction) -> None:
        """Activate items."""


class HealingConsumable(BaseConsumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: yarl.actions.UseItemAction) -> None:
        consumer = action.entity

        amount_recovered = consumer.combatant.heal(self.amount)
        if amount_recovered > 0:
            self.engine.message_log.append(
                f"You consume the {self.parent.name} and recover {amount_recovered} HP!",
                colors.HEALTH_RECOVERED,
            )
        else:
            raise ImpossibleActionError("You're already at full health.")
