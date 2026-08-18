import numpy as np
import tcod

import yarl.action
import yarl.actions
import yarl.entity


class BaseAI(yarl.actions.BaseAction):
    entity: yarl.entity.Actor

    def get_path_to(self, x: int, y: int) -> list[tuple[int, int]]:
        cost = np.array(self.entity.parent.tiles["walkable"], dtype=np.int8)

        for e in self.entity.parent.entities:
            if e.blocks_movement and cost[e.x, e.y]:
                cost[e.x, e.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))
        path: list[list[int]] = pathfinder.path_to((x, y))[1:].tolist()

        # Convert from list[list[int]] to list[tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: yarl.entity.Actor):
        super().__init__(entity)
        self.path: list[tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return yarl.actions.MeleeAttackAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return yarl.actions.MoveAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        return yarl.actions.WaitAction(self.entity).perform()
