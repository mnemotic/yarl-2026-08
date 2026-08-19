from os import path

import tcod

YARL_ASSET_DIR = path.abspath(path.join(path.dirname(__file__), "assets"))
assert path.exists(YARL_ASSET_DIR)

__version__ = "0.8.1"

tcod.lib.SDL_SetAppMetadata(
    b"YARL",
    bytes(__version__.encode()),
    b"dev.mnemotic.yarl2026",
)
