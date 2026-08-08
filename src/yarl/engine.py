from collections.abc import Iterable
from collections.abc import Set as AbstractSet
from typing import Any

from tcod.console import Console
from tcod.context import Context

from yarl.entity import Entity
from yarl.game_map import GameMap
from yarl.input_handlers import EventHandler
from yarl.state import State


class Engine:
    entities: AbstractSet[Entity]
    event_handler: State
    game_map: GameMap
    player: Entity

    def __init__(
        self,
        entities: AbstractSet[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        for entity in self.entities:
            console.print(
                x=entity.x, y=entity.y, text=chr(entity.char), fg=entity.color
            )
        context.present(console)
        console.clear(ch=ord("."), fg=(255 // 2, 255 // 2, 255 // 2))
