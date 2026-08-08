from typing import Any

import numpy as np
import numpy.typing as npt
from tcod.console import Console

import yarl.tile_types as tiles


class GameMap:
    width: int
    height: int
    tiles: npt.NDArray[Any]

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=tiles.floor, order="F")
        self.tiles[30:33, 22] = tiles.wall

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0 : self.width, 0 : self.height] = self.tiles["obscured"]
