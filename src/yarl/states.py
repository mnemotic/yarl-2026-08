from abc import ABC, abstractmethod

import tcod.event
from tcod.console import Console
from tcod.event import Event, KeyDown, KeySym

import yarl.action
import yarl.actions
import yarl.engine
from yarl.colors import IMPOSSIBLE
from yarl.exceptions import ImpossibleActionError

MOVE_KEYS = {
    # Arrow keys.
    KeySym.UP: (0, -1),
    KeySym.DOWN: (0, 1),
    KeySym.LEFT: (-1, 0),
    KeySym.RIGHT: (1, 0),
    KeySym.HOME: (-1, -1),
    KeySym.END: (-1, 1),
    KeySym.PAGEUP: (1, -1),
    KeySym.PAGEDOWN: (1, 1),
    # Numpad keys.
    KeySym.KP_1: (-1, 1),
    KeySym.KP_2: (0, 1),
    KeySym.KP_3: (1, 1),
    KeySym.KP_4: (-1, 0),
    KeySym.KP_6: (1, 0),
    KeySym.KP_7: (-1, -1),
    KeySym.KP_8: (0, -1),
    KeySym.KP_9: (1, -1),
    # Vi keys.
    KeySym.H: (-1, 0),
    KeySym.J: (0, 1),
    KeySym.K: (0, -1),
    KeySym.L: (1, 0),
    KeySym.Y: (-1, -1),
    KeySym.U: (1, -1),
    KeySym.B: (-1, 1),
    KeySym.N: (1, 1),
}

WAIT_KEYS = {
    KeySym.PERIOD,
    KeySym.KP_5,
    KeySym.CLEAR,
}


CURSOR_Y_KEYS = {
    KeySym.UP: -1,
    KeySym.DOWN: 1,
    KeySym.PAGEUP: -10,
    KeySym.PAGEDOWN: 10,
}


class BaseState(ABC):
    def __init__(self, engine: yarl.engine.Engine):
        self.engine = engine

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        match event:
            case KeyDown(sym=KeySym.ESCAPE):
                raise SystemExit()
            case _:
                self.handle_action(self.dispatch(event))

    @abstractmethod
    def handle_action(self, action: yarl.action.Action | None) -> bool:
        """
        Handle actions returned by dispatch.

        Returns `True` fi the action should advance a turn.
        """
        if action is None:
            return False

        try:
            action.perform()
        except ImpossibleActionError as err:
            self.engine.message_log.append(err.args[0], IMPOSSIBLE)
            return False

        self.engine.handle_npc_turns()
        self.engine.update_fov()

        return True

    @abstractmethod
    def dispatch(self, event: Event) -> yarl.action.Action | None: ...

    @abstractmethod
    def render(self, console: Console) -> None:
        self.engine.render(console)


class MainGameState(BaseState):
    def handle_event(self, event: Event) -> None:
        match event:
            case KeyDown(sym=KeySym.V):
                self.engine.state = JournalViewer(self.engine)
            case _:
                super().handle_event(event)

    def handle_action(self, action: yarl.action.Action | None) -> bool:
        return super().handle_action(action)

    def dispatch(self, event: Event) -> yarl.action.Action | None:
        action: yarl.action.Action | None = None

        engine = self.engine
        player = engine.player

        match event:
            case KeyDown() as e if e.sym in MOVE_KEYS:
                action = yarl.actions.BumpAction(player, *MOVE_KEYS[e.sym])
            case KeyDown() as e if e.sym in WAIT_KEYS:
                action = yarl.actions.WaitAction(player)

        return action

    def render(self, console: Console) -> None:
        super().render(console)


class GameOverState(BaseState):
    def handle_event(self, event: Event) -> None:
        match event:
            case KeyDown(sym=KeySym.V):
                self.engine.state = JournalViewer(self.engine)
            case _:
                super().handle_event(event)

    def handle_action(self, action: yarl.action.Action | None) -> bool:
        return super().handle_action(action)

    def dispatch(self, event: Event) -> yarl.action.Action | None:
        return None

    def render(self, console: Console) -> None:
        super().render(console)


class JournalViewer(BaseState):
    def __init__(self, engine: yarl.engine.Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def handle_event(self, event: Event) -> None:
        match event:
            case KeyDown(sym=sym) if sym in CURSOR_Y_KEYS:
                delta = CURSOR_Y_KEYS[sym]
                if delta < 0 and self.cursor == 0:
                    self.cursor = self.log_length - 1
                elif delta > 0 and self.cursor == self.log_length - 1:
                    self.cursor = 0
                else:
                    self.cursor = max(0, min(self.cursor + delta, self.log_length - 1))
            case KeyDown(sym=KeySym.HOME):
                self.cursor = 0
            case KeyDown(sym=KeySym.END):
                self.cursor = self.log_length - 1
            case KeyDown(sym=KeySym.ESCAPE):
                self.engine.state = MainGameState(self.engine)

    def handle_action(self, action: yarl.action.Action | None) -> bool:
        return super().handle_action(action)

    def dispatch(self, event: Event) -> yarl.action.Action | None:
        return None

    def render(self, console: Console) -> None:
        super().render(console)

        log_console = Console(console.width - 6, console.height - 6)
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print(
            x=0,
            y=0,
            width=log_console.width,
            height=1,
            text="┤Message history├",
            alignment=tcod.lib.TCOD_CENTER,
        )

        self.engine.message_log.print_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)
