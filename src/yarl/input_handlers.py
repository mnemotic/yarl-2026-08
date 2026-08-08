import tcod.event

from yarl.action import Action
from yarl.actions import MoveAction, QuitAction


class EventHandler:
    def dispatch(self, event: tcod.event.Event) -> Action | None:
        action: Action | None = None

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.KeyDown(sym=tcod.event.KeySym.UP):
                action = MoveAction(dy=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.DOWN):
                action = MoveAction(dy=+1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.LEFT):
                action = MoveAction(dx=-1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RIGHT):
                action = MoveAction(dx=+1)

            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = QuitAction()

        return action
