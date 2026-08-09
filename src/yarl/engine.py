from collections.abc import Iterable
from collections.abc import Set as AbstractSet
from typing import Any

import tcod
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
        entities: AbstractSet[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities: AbstractSet[Entity] = entities
        self.event_handler: State = event_handler
        self.game_map: GameMap = game_map
        self.player: Entity = player

        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)
            self.update_fov()

    def update_fov(self) -> None:
        """Recompute the visible are based on player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for entity in self.entities:
            if not self.game_map.visible[entity.x, entity.y]:
                continue
            console.print(
                x=entity.x, y=entity.y, text=chr(entity.char), fg=entity.color
            )
        context.present(console)
        console.clear(ch=ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
