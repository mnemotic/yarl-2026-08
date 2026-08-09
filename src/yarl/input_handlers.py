import tcod.event

import yarl.action
import yarl.actions
import yarl.engine

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.KeySym.UP: (0, -1),
    tcod.event.KeySym.DOWN: (0, 1),
    tcod.event.KeySym.LEFT: (-1, 0),
    tcod.event.KeySym.RIGHT: (1, 0),
    tcod.event.KeySym.HOME: (-1, -1),
    tcod.event.KeySym.END: (-1, 1),
    tcod.event.KeySym.PAGEUP: (1, -1),
    tcod.event.KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.KeySym.KP_1: (-1, 1),
    tcod.event.KeySym.KP_2: (0, 1),
    tcod.event.KeySym.KP_3: (1, 1),
    tcod.event.KeySym.KP_4: (-1, 0),
    tcod.event.KeySym.KP_6: (1, 0),
    tcod.event.KeySym.KP_7: (-1, -1),
    tcod.event.KeySym.KP_8: (0, -1),
    tcod.event.KeySym.KP_9: (1, -1),
    # Vi keys.
    tcod.event.KeySym.H: (-1, 0),
    tcod.event.KeySym.J: (0, 1),
    tcod.event.KeySym.K: (0, -1),
    tcod.event.KeySym.L: (1, 0),
    tcod.event.KeySym.Y: (-1, -1),
    tcod.event.KeySym.U: (1, -1),
    tcod.event.KeySym.B: (-1, 1),
    tcod.event.KeySym.N: (1, 1),
}

WAIT_KEYS = {
    tcod.event.KeySym.PERIOD,
    tcod.event.KeySym.KP_5,
    tcod.event.KeySym.CLEAR,
}


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

            case tcod.event.KeyDown() as e if e.sym in MOVE_KEYS:
                action = yarl.actions.BumpAction(player, *MOVE_KEYS[e.sym])
            case tcod.event.KeyDown() as e if e.sym in WAIT_KEYS:
                action = yarl.actions.WaitAction(player)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = yarl.actions.QuitAction(player)

        return action
