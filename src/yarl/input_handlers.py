import tcod.event

from yarl.action import Action
from yarl.actions import BumpAction, QuitAction


class EventHandler:
    def dispatch(self, event: tcod.event.Event) -> Action | None:
        action: Action | None = None

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = BumpAction(dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = BumpAction(dy=+1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = BumpAction(dx=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = BumpAction(dx=+1)

            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = QuitAction()

        return action
