from abc import ABC, abstractmethod

import yarl.engine
import yarl.entity
from yarl import colors
from yarl.exceptions import ImpossibleActionError


class BaseAction(ABC):
    def __init__(self, entity: yarl.entity.Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> yarl.engine.Engine:
        return self.entity.parent.engine

    @abstractmethod
    def perform(self) -> None: ...


class DirectionalAction(BaseAction):
    def __init__(self, entity: yarl.entity.Actor, dx: int = 0, dy: int = 0):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> yarl.entity.Entity | None:
        return self.engine.game_map.get_blocking_entity_at(*self.dest_xy)

    @property
    def target_actor(self) -> yarl.entity.Actor | None:
        return self.engine.game_map.get_actor_at(*self.dest_xy)


class BumpAction(DirectionalAction):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAttackAction(self.entity, self.dx, self.dy).perform()
        else:
            return MoveAction(self.entity, self.dx, self.dy).perform()


class MeleeAttackAction(DirectionalAction):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise ImpossibleActionError("Nothing to attack.")

        log = self.engine.message_log

        damage = self.entity.combatant.power - target.combatant.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            color = colors.PLAYER_ATK
        else:
            color = colors.ENEMY_ATK
        if damage > 0:
            log.append(f"{attack_desc} for {damage} hit points.", color)
            target.combatant.hp -= damage
        else:
            log.append(f"{attack_desc} but does not damage.", color)


class MoveAction(DirectionalAction):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise ImpossibleActionError("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise ImpossibleActionError("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise ImpossibleActionError("That way is blocked.")
        self.entity.move(self.dx, self.dy)


class WaitAction(BaseAction):
    def perform(self) -> None:
        pass


class UseItemAction(BaseAction):
    def __init__(
        self,
        entity: yarl.entity.Actor,
        item: yarl.entity.Item,
        target: tuple[int, int] | None = None,
    ):
        super().__init__(entity)
        self.item = item
        if not target:
            target = entity.x, entity.y
        self.target = target

    @property
    def target_actor(self) -> yarl.entity.Actor | None:
        return self.engine.game_map.get_actor_at(*self.target)

    def perform(self) -> None:
        self.item.consumable.activate(self)


class PickUpItemAction(BaseAction):
    def __init__(self, entity: yarl.entity.Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_x = self.entity.x
        actor_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_x == item.x and actor_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise ImpossibleActionError("Your inventory is full.")

                # Remove the item from the map and put it into the inventory.
                self.engine.game_map.entities.remove(item)
                item.parent = inventory
                inventory.items.append(item)

                self.engine.message_log.append(f"You picked up the {item.name}!")
                return
        raise ImpossibleActionError("There's nothing to pick up here.")


class DropItemAction(UseItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)
