from tcod import libtcodpy
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

import yarl.entity
import yarl.game_map
import yarl.input_handlers
from yarl.state import State


class Engine:
    game_map: yarl.game_map.GameMap

    def __init__(
        self,
        player: yarl.entity.Actor,
    ):
        self.event_handler: State = yarl.input_handlers.MainGameEventHandler(self)
        self.player: yarl.entity.Actor = player

    def handle_npc_turns(self) -> None:
        for e in set(self.game_map.actors) - {self.player}:
            if e.ai:
                e.ai.perform()
            print(f"The {e.name} wonders when it will get to take a real turn.")

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

        # Status bar.
        console.print(
            x=1,
            y=47,
            text=f"HP: {self.player.combatant.hp:^4} / {self.player.combatant.max_hp:^4}",
            fg=(255, 255, 255),
        )

        context.present(console)
        console.clear(ch=ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
