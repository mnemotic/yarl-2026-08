import tcod.event
from tcod.console import Console
from tcod.context import Context

import yarl.action
import yarl.actions
import yarl.engine
from yarl.utils import get_content_scale, get_window_size

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


CURSOR_Y_KEYS = {
    tcod.event.KeySym.UP: -1,
    tcod.event.KeySym.DOWN: 1,
    tcod.event.KeySym.PAGEUP: -10,
    tcod.event.KeySym.PAGEDOWN: 10,
}


class BaseState:
    def __init__(self, engine: yarl.engine.Engine):
        self.engine = engine

    def handle_events(self, context: Context) -> None: ...

    def on_render(self, console: Console) -> None:
        self.engine.render(console)

    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None: ...


class MainGameState(BaseState):
    def handle_events(self, context: Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            match event:
                case tcod.event.MouseMotion(tile=tile):
                    x, y = tile
                    if self.engine.game_map.in_bounds(x, y):
                        self.engine.cursor_position = x, y
                    else:
                        self.engine.cursor_position = None
                    continue

            action = self.dispatch(event)
            if action is None:
                continue

            action.perform()

            self.engine.handle_npc_turns()
            self.engine.update_fov()

    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None:
        action: yarl.action.Action | None = None

        engine = self.engine
        player = engine.player

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.WindowEvent(
                type="DisplayScaleChanged", window_id=window_id
            ):
                sdl_window_p = tcod.lib.SDL_GetWindowFromID(window_id)
                display_id = tcod.lib.SDL_GetDisplayForWindow(sdl_window_p)
                engine.content_scale = get_content_scale(display_id)

                context = engine.context
                if context.sdl_window is not None:
                    context.sdl_window.size = get_window_size(
                        display_id,
                        engine.tileset,
                        engine.con_width,
                        engine.con_height,
                    )

            case tcod.event.KeyDown() as e if e.sym in MOVE_KEYS:
                action = yarl.actions.BumpAction(player, *MOVE_KEYS[e.sym])
            case tcod.event.KeyDown() as e if e.sym in WAIT_KEYS:
                action = yarl.actions.WaitAction(player)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = yarl.actions.QuitAction(player)

            case tcod.event.KeyDown(sym=tcod.event.KeySym.V):
                self.engine.state = JournalViewer(self.engine)

        return action


class GameOverState(BaseState):
    def handle_events(self, context: Context) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()

    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None:
        action: yarl.action.Action | None = None

        match event:
            case tcod.event.Quit():
                raise SystemExit()

            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                action = yarl.actions.QuitAction(self.engine.player)

        return action


class JournalViewer(BaseState):
    def __init__(self, engine: yarl.engine.Engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: Console) -> None:
        super().on_render(console)

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

    def dispatch(self, event: tcod.event.Event) -> yarl.action.Action | None:
        return None

    def handle_events(self, context: Context) -> None:
        for event in tcod.event.get():
            match event:
                case tcod.event.KeyDown(sym=sym) if sym in CURSOR_Y_KEYS:
                    delta = CURSOR_Y_KEYS[sym]
                    if delta < 0 and self.cursor == 0:
                        self.cursor = self.log_length - 1
                    elif delta > 0 and self.cursor == self.log_length - 1:
                        self.cursor = 0
                    else:
                        self.cursor = max(
                            0, min(self.cursor + delta, self.log_length - 1)
                        )
                case tcod.event.KeyDown(sym=tcod.event.KeySym.HOME):
                    self.cursor = 0
                case tcod.event.KeyDown(sym=tcod.event.KeySym.END):
                    self.cursor = self.log_length - 1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                    self.engine.state = MainGameState(self.engine)
