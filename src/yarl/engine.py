from collections.abc import Iterable
from typing import Any

from tcod import libtcodpy
from tcod.console import Console
from tcod.context import Context
from tcod.map import compute_fov

from yarl.entity import Entity
from yarl.game_map import GameMap
from yarl.input_handlers import EventHandler
from yarl.state import State


class Engine:
    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.event_handler: State = event_handler
        self.game_map: GameMap = game_map
        self.player: Entity = player

        self.update_fov()

    def handle_npc_turns(self) -> None:
        for e in self.game_map.entities - {self.player}:
            print(f"The {e.name} wonders when it will get to take a real turn.")

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)
            self.handle_npc_turns()
            self.update_fov()

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
        context.present(console)
        console.clear(ch=ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
