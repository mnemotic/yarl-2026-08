from abc import ABC

import yarl.engine
import yarl.entity
import yarl.game_map


class BaseComponent(ABC):
    parent: yarl.entity.Entity

    @property
    def game_map(self) -> yarl.game_map.GameMap:
        return self.parent.game_map

    @property
    def engine(self) -> yarl.engine.Engine:
        return self.game_map.engine
