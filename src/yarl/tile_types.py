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
        ("walkable", np.bool),
        ("opaque", np.bool),
        ("obscured", graphic_dt),
    ]
)


def new_tile(
    *,
    walkable: int,
    opaque: int,
    obscured: tuple[int, tuple[int, int, int], tuple[int, int, int]],
) -> np.ndarray:
    return np.array((walkable, opaque, obscured), dtype=tile_dt)


floor = new_tile(
    walkable=True, opaque=False, obscured=(ord(" "), (255, 255, 255), (50, 50, 150))
)

wall = new_tile(
    walkable=False, opaque=True, obscured=(ord("\u2593"), (255, 255, 255), (0, 0, 100))
)
