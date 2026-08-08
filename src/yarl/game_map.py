from typing import Any

import numpy as np
from tcod.console import Console

import yarl.tile_types as tiles


class GameMap:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.tiles: np.ndarray[tuple[int, int], Any] = np.full(
            (width, height), fill_value=tiles.wall, order="F"
        )

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["obscured"]
