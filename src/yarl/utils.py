from typing import Any

import tcod
from tcod.tileset import Tileset


def get_content_scale(display_id: Any) -> float:
    s = tcod.lib.SDL_GetDisplayContentScale(display_id)
    return s


def get_window_size(
    display_id: Any, tileset: Tileset, columns: int, rows: int
) -> tuple[int, int]:
    s = get_content_scale(display_id)
    w = int(columns * tileset.tile_width * s)
    h = int(rows * tileset.tile_height * s)
    return w, h
