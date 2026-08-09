import copy
from typing import Self

from yarl.game_map import GameMap


class Entity:
    """Generic game object representing player chareacters, NPCs, items, etc."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: int = ord("?"),
        color: tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self, game_map: GameMap, x: int, y: int) -> Self:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        game_map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
