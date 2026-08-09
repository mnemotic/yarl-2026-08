import copy
from typing import Self

from yarl.game_map import GameMap


class Entity:
    """Generic game object representing player chareacters, NPCs, items, etc."""

    game_map: GameMap

    def __init__(
        self,
        game_map: GameMap | None = None,
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
        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self, game_map: GameMap, x: int, y: int) -> Self:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)
        return clone

    def place(self, x: int, y: int, game_map: GameMap | None = None) -> None:
        self.x = x
        self.y = y
        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
