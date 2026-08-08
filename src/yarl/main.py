from importlib.resources import as_file, files
from pathlib import Path

import tcod

KEY_COMMANDS = {
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, +1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (+1, 0),
}


def main() -> None:
    screen_width = 80
    screen_height = 50

    player_x = screen_width // 2
    player_y = screen_height // 2

    with as_file(files("yarl.assets").joinpath("zilk_16x16.png")) as f:
        tileset_filepath = f
        tileset = tcod.tileset.load_tilesheet(
            Path(tileset_filepath),
            16,
            16,
            tcod.tileset.CHARMAP_CP437,
        )

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="YARL",
        vsync=True,
    ) as context:
        root_console = context.new_console()
        while True:
            root_console.clear(ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
            root_console.print(x=player_x, y=player_y, text="@", fg=(255, 255, 255))
            context.present(root_console)
            for event in tcod.event.wait():
                match event:
                    case tcod.event.KeyDown(sym=sym) if sym in KEY_COMMANDS:
                        player_x += KEY_COMMANDS[sym][0]
                        player_y += KEY_COMMANDS[sym][1]
                    case tcod.event.Quit():
                        raise SystemExit()
