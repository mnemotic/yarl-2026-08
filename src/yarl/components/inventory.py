import yarl.entity
from yarl.components.base_component import BaseComponent


class Inventory(BaseComponent):
    parent: yarl.entity.Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: list[yarl.entity.Item] = []

    # TODO: Dropping an item should be an action.
    def drop(self, item: yarl.entity.Item) -> None:
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.game_map)
        self.engine.message_log.append(f"You dropped the {item.name}.")
