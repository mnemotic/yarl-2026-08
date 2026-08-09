import tcod.event

import yarl.action
import yarl.actions
import yarl.engine


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

    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None:
        action: yarl.action.Action | None = None

        player = self.engine.player

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = yarl.actions.BumpAction(player, dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = yarl.actions.BumpAction(player, dy=+1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = yarl.actions.BumpAction(player, dx=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = yarl.actions.BumpAction(player, dx=+1)

            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = yarl.actions.QuitAction(player)

        return action
