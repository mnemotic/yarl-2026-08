import tcod.event

import yarl.engine
from yarl.action import Action
from yarl.actions import BumpAction, QuitAction


class EventHandler:
    def __init__(self, engine: yarl.engine.Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue

            action.perform()

            self.engine.handle_npc_turns()
            self.engine.update_fov()

    def dispatch(self, event: tcod.event.Event) -> Action | None:
        action: Action | None = None

        player = self.engine.player

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = BumpAction(player, dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = BumpAction(player, dy=+1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = BumpAction(player, dx=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = BumpAction(player, dx=+1)

            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = QuitAction(player)

        return action
