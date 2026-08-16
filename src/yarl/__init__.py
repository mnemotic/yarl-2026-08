from importlib.metadata import version

import tcod

assert __package__ is not None
__version__ = version(__package__)


tcod.lib.SDL_SetAppMetadata(
    bytes(__package__.encode()),
    bytes(__version__.encode()),
    b"dev.mnemotic.yarl-202608",
)
