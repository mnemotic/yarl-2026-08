import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        # `True` when the tile can be traversed by walking capability.
        ("walkable", np.bool),
        # `True` when the tile does NOT block field-of-view.
        ("transparent", np.bool),
        # Graphic for when the tile is NOT in field-of-view.
        (
            "obscured",
            graphic_dt,
        ),
        # Graphic for when the tile is in field-of-view.
        (
            "visible",
            graphic_dt,
        ),
    ]
)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


def new_tile(
    *,
    walkable: int,
    transparent: int,
    obscured: tuple[int, tuple[int, int, int], tuple[int, int, int]],
    visible: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, transparent, obscured, visible), dtype=tile_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    obscured=(ord("."), (255, 255, 255), (50, 50, 150)),
    visible=(ord("."), (255, 255, 255), (200, 180, 50)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    obscured=(ord("\u2593"), (255, 255, 255), (0, 0, 100)),
    visible=(ord("\u2593"), (255, 255, 255), (130, 110, 50)),
)
