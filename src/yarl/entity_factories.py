import yarl.entity
from yarl.components.ai import HostileEnemy
from yarl.components.combatant import Combatant
from yarl.components.consumables import HealingConsumable
from yarl.components.inventory import Inventory

player = yarl.entity.Actor(
    char=ord("@"),
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

goblin = yarl.entity.Actor(
    char=ord("g"),
    color=(63, 127, 63),
    name="Goblin",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)

orc = yarl.entity.Actor(
    char=ord("o"),
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    combatant=Combatant(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)

healing_potion = yarl.entity.Item(
    char=ord("!"),
    color=(127, 0, 255),
    name="Healing Potion",
    consumable=HealingConsumable(4),
)
