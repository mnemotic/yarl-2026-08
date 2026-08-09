import yarl.engine
import yarl.entity


class BaseAction:
    pass


class QuitAction(BaseAction):
    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        raise SystemExit()


class DirectionalAction(BaseAction):
    def __init__(self, *, dx: int = 0, dy: int = 0):
        super().__init__()

        self.dx = dx
        self.dy = dy


class BumpAction(DirectionalAction):
    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return MeleeAttackAction(dx=self.dx, dy=self.dy).perform(engine, entity)
        else:
            return MoveAction(dx=self.dx, dy=self.dy).perform(engine, entity)


class MeleeAttackAction(DirectionalAction):
    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity_at(dest_x, dest_y)
        if not target:
            return

        print(f"You kick the {target.name}, much to its annoyance!")


class MoveAction(DirectionalAction):
    def perform(self, engine: yarl.engine.Engine, entity: yarl.entity.Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if engine.game_map.get_blocking_entity_at(dest_x, dest_y):
            return
        entity.move(self.dx, self.dy)
