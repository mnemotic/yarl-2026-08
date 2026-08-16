import tcod
from tcod import libtcodpy
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov
from tcod.tileset import Tileset

import yarl.entity
import yarl.game_map
import yarl.states
from yarl.message_log import MessageLog
from yarl.state import State
from yarl.ui import draw_hp_bar
from yarl.utils import get_content_scale


class Engine:
    game_map: yarl.game_map.GameMap

    def __init__(
        self,
        player: yarl.entity.Actor,
        context: Context,
        tileset: Tileset,
        con_width: int,
        con_height: int,
    ):
        self.state: State = yarl.states.MainGameState(self)
        self.message_log = MessageLog()
        self.player = player
        self.context = context
        self.tileset = tileset
        self.con_width = con_width
        self.con_height = con_height

        display_id = tcod.lib.SDL_GetDisplayForWindow(self.context.sdl_window_p)
        self.content_scale = get_content_scale(display_id)

    def handle_npc_turns(self) -> None:
        for e in set(self.game_map.actors) - {self.player}:
            if e.ai:
                e.ai.perform()

    def update_fov(self) -> None:
        """Recompute the visible are based on player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
            algorithm=libtcodpy.FOV_SYMMETRIC_SHADOWCAST,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        self.message_log.print(console=console, x=21, y=45, width=40, height=5)

        draw_hp_bar(
            console=console,
            x=0,
            y=45,
            value=self.player.combatant.hp,
            max_value=self.player.combatant.max_hp,
            width=20,
        )

        context.present(console)
        console.clear(ch=ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
