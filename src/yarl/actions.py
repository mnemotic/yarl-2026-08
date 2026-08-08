import yarl.engine
import yarl.entity
from yarl.action import Action


class BaseAction(Action):
    pass


class QuitAction(BaseAction):
    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        raise SystemExit()


class MoveAction(BaseAction):
    def __init__(self, *, dx: int = 0, dy: int = 0):
        super().__init__()

        self.dx: int = dx
        self.dy: int = dy

    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        entity.move(self.dx, self.dy)
