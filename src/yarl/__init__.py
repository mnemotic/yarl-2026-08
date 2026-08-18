import sys
from os import path

import tcod

YARL_DATA_DIR = sys._MEIPASS if hasattr(sys, "_MEIPASS") else path.dirname(__file__)
YARL_ASSET_DIR = path.abspath(path.join(YARL_DATA_DIR, "assets"))

__version__ = "0.6.0"

tcod.lib.SDL_SetAppMetadata(
    b"YARL",
    bytes(__version__.encode()),
    b"dev.mnemotic.yarl2026",
)
