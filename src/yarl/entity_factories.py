import yarl.entity
from yarl.components.ai import HostileEnemy
from yarl.components.combatant import Combatant

player = yarl.entity.Actor(
    char=ord("@"),
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=30, defense=2, power=5),
)

goblin = yarl.entity.Actor(
    char=ord("g"),
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=10, defense=0, power=3),
)

orc = yarl.entity.Actor(
    char=ord("o"),
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=16, defense=1, power=4),
)
