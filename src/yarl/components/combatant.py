import yarl.entity
from yarl import colors
from yarl.components.base_component import BaseComponent
from yarl.render_order import RenderOrder
from yarl.states import GameOverState


class Combatant(BaseComponent):
    parent: yarl.entity.Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.parent:
            message = "You died!"
            color = colors.PLAYER_DIE
            self.engine.state = GameOverState(self.engine)
        else:
            message = f"{self.parent.name} is dead!"
            color = colors.ENEMY_DIE

        self.parent.char = ord("%")
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.append(message, color)
