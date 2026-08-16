from tcod.console import Console

import yarl.engine
import yarl.game_map
from yarl import colors


def get_names_at_tile(x: int, y: int, map: yarl.game_map.GameMap) -> str | None:
    if not map.in_bounds(x, y) or not map.visible[x, y]:
        return None
    names = ", ".join(e.name for e in map.entities if e.x == x and e.y == y)
    return names.capitalize()


def draw_hp_bar(
    console: Console, x: int, y: int, value: int, max_value: int, width: int
) -> None:
    fill_width = int(float(value) / max_value * width)

    console.draw_rect(x=x, y=y, width=width, height=1, ch=1, bg=colors.HP_BAR_EMPTY)
    if fill_width > 0:
        console.draw_rect(
            x=x, y=y, width=fill_width, height=1, ch=1, bg=colors.HP_BAR_FILL
        )
    console.print(
        x=x + 1, y=y, text=f"HP: {value:^4} / {max_value:^4}", fg=colors.HP_BAR_TEXT
    )


def draw_names_at_cursor(
    console: Console, x: int, y: int, engine: yarl.engine.Engine
) -> None:
    if engine.cursor_position is None:
        return
    cx, cy = engine.cursor_position
    names = get_names_at_tile(cx, cy, engine.game_map)
    if names is None:
        return
    console.print(x=x, y=y, text=names)
