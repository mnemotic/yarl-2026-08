from importlib.resources import as_file, files
from pathlib import Path

import tcod

from yarl.engine import Engine
from yarl.entity import Entity
from yarl.game_map import GameMap
from yarl.input_handlers import EventHandler

KEY_COMMANDS = {
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, +1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (+1, 0),
}


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    with as_file(files("yarl.assets").joinpath("zilk_16x16.png")) as f:
        tileset_filepath = f
        tileset = tcod.tileset.load_tilesheet(
            Path(tileset_filepath),
            16,
            16,
            tcod.tileset.CHARMAP_CP437,
        )

    player = Entity(screen_width // 2, screen_height // 2, ord("@"), (255, 255, 255))
    rat = Entity(screen_width // 2 - 5, screen_height // 2, ord("r"), (255, 255, 0))
    entities = {player, rat}

    game_map = GameMap(map_width, map_height)
    event_handler = EventHandler()
    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="YARL",
        vsync=True,
    ) as context:
        root_console = context.new_console(order="F")
        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)
