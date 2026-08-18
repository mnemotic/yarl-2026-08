import traceback
from copy import deepcopy
from pathlib import Path

import tcod

import yarl.entity_factories
from yarl import YARL_ASSET_DIR, __version__, colors
from yarl.engine import Engine
from yarl.procgen import generate_dungeon
from yarl.utils import get_content_scale, get_window_size


def get_asset_path(asset: str) -> Path:
    asset_dir = Path(YARL_ASSET_DIR)
    asset_path = asset_dir.joinpath(asset)

    return asset_path


def main() -> None:
    # Console width and height, in tiles.
    con_width = 80
    con_height = 50

    # Map width and height, in tiles.
    map_width = 80
    map_height = 43

    # Min and max room dimensions, in tiles.
    room_max_size = 10
    room_min_size = 6

    # Maximum number of rooms in a map.
    max_rooms = 30

    # Maximum number of monsters per map [0, max_monsters_per_room].
    max_monsters_per_room = 2

    tileset_path = get_asset_path("zilk_16x16.png")
    tileset = tcod.tileset.load_tilesheet(
        tileset_path,
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    #
    # Calculate window size, taking into account high DPI scaling, if any.
    #

    tcod.lib.SDL_Init(tcod.lib.SDL_INIT_VIDEO)
    display_id = tcod.lib.SDL_GetPrimaryDisplay()
    # Window size, in pixels.
    wnd_width, wnd_height = get_window_size(display_id, tileset, con_width, con_height)

    with tcod.context.new(
        width=wnd_width,
        height=wnd_height,
        # columns=con_width,
        # rows=con_height,
        tileset=tileset,
        title="YARL",
        vsync=True,
        sdl_window_flags=0,  # Make the window non-resizable.
    ) as context:
        player = deepcopy(yarl.entity_factories.player)

        engine = Engine(player, context, tileset, con_width, con_height)
        engine.game_map = generate_dungeon(
            map_height=map_height,
            map_width=map_width,
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            max_monsters_per_room=max_monsters_per_room,
            engine=engine,
        )
        engine.update_fov()
        engine.message_log.append(f"YARL - Yet Another Roguelike v{__version__}")
        engine.message_log.append(
            "Hello and welcome, adventurer, to yet another dungeon!",
            colors.WELCOME_TEXT,
        )

        scale = get_content_scale(display_id)
        console = context.new_console(order="F", magnification=scale)
        while True:
            # Create a new console if the scale has changed.
            #
            # There is no way to change the scale of an existing console?
            if engine.content_scale != scale:
                scale = engine.content_scale
                console = context.new_console(order="F", magnification=scale)

            console.clear()
            engine.state.render(console)
            context.present(console)
            try:
                for event in tcod.event.get():
                    match event:
                        case tcod.event.Quit():
                            raise SystemExit()

                        case tcod.event.WindowEvent(
                            type="DisplayScaleChanged", window_id=window_id
                        ):
                            sdl_window_p = tcod.lib.SDL_GetWindowFromID(window_id)
                            display_id = tcod.lib.SDL_GetDisplayForWindow(sdl_window_p)
                            engine.content_scale = get_content_scale(display_id)

                            context = engine.context
                            if context.sdl_window is not None:
                                context.sdl_window.size = get_window_size(
                                    display_id,
                                    engine.tileset,
                                    engine.con_width,
                                    engine.con_height,
                                )
                        case _:
                            context.convert_event(event)
                            engine.state.handle_event(event)
            except Exception:  # noqa: BLE001
                traceback.print_exc()
                engine.message_log.append(traceback.format_exc(), colors.ERROR)
