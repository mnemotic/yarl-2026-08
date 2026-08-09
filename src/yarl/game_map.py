from collections.abc import Iterable

import numpy as np
from tcod.console import Console

import yarl.engine
import yarl.entity
import yarl.tile_types as tiles


class GameMap:
    def __init__(
        self,
        engine: yarl.engine.Engine,
        width: int,
        height: int,
        entities: Iterable[yarl.entity.Entity] = (),
    ):
        self.engine = engine
        self.width: int = width
        self.height: int = height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tiles.wall, order="F")

        # Tiles that the player can see.
        # TODO: At least `visible` should live on the entity, as its "viewshed".
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at(self, x: int, y: int) -> yarl.entity.Entity | None:
        for e in self.entities:
            if e.blocks_movement and e.x == x and e.y == y:
                return e
        return None

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "visible" colors.
        If it isn't in the "visible" array, but it's in the "explored" array, then draw
        it with the "obscured" colors. Otherwise, the default is "SHROUD".
        """
        console.rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["visible"], self.tiles["obscured"]],
            default=tiles.SHROUD,
        )
        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, text=chr(entity.char), fg=entity.color
                )
