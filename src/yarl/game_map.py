import numpy as np
from tcod.console import Console

import yarl.tile_types as tiles


class GameMap:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.tiles = np.full((width, height), fill_value=tiles.wall, order="F")

        # Tiles that the player can see.
        # TODO: At least `visible` should live on the entity, as its "viewshed".
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

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
