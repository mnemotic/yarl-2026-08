import copy
from typing import Self

import yarl.consumable
from yarl.components import ai
from yarl.components.combatant import Combatant
from yarl.game_map import GameMap
from yarl.render_order import RenderOrder


class Entity:
    """Generic game object representing player chareacters, NPCs, items, etc."""

    parent: GameMap

    def __init__(
        self,
        parent: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        char: int = ord("?"),
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            self.parent = parent
            parent.entities.add(self)

    @property
    def game_map(self) -> GameMap:
        return self.parent.game_map

    def spawn(self, game_map: GameMap, x: int, y: int) -> Self:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, game_map: GameMap | None = None) -> None:
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "parent") and self.parent is self.game_map:
                self.game_map.entities.remove(self)
            self.parent = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: int = ord("?"),
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: type[ai.BaseAI],
        combatant: Combatant,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )
        self.ai: ai.BaseAI | None = ai_cls(self)
        self.combatant = combatant
        self.combatant.parent = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: int = ord("?"),
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: yarl.consumable.Consumable,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.consumable.parent = self
