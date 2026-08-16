from tcod.console import Console

from yarl import colors


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
