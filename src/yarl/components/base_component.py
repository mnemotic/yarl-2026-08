import yarl.engine
import yarl.entity


class BaseComponent:
    entity: yarl.entity.Entity

    @property
    def engine(self) -> yarl.engine.Engine:
        return self.entity.game_map.engine
