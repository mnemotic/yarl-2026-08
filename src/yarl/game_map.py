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

    @property
    def game_map(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterable[yarl.entity.Actor]:
        yield from (
            e for e in self.entities if isinstance(e, yarl.entity.Actor) and e.is_alive
        )

    @property
    def items(self) -> Iterable[yarl.entity.Item]:
        yield from (e for e in self.entities if isinstance(e, yarl.entity.Item))

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at(self, x: int, y: int) -> yarl.entity.Entity | None:
        for e in self.entities:
            if e.blocks_movement and e.x == x and e.y == y:
                return e
        return None

    def get_actor_at(self, x: int, y: int) -> yarl.entity.Actor | None:
        for a in self.actors:
            if a.x == x and a.y == y:
                return a
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

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for e in entities_sorted_for_rendering:
            if self.visible[e.x, e.y]:
                console.print(x=e.x, y=e.y, text=chr(e.char), fg=e.color)
