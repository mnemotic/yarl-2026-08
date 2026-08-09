from yarl import entity

player = entity.Entity(
    char=ord("@"), color=(255, 255, 255), name="Player", blocks_movement=True
)

goblin = entity.Entity(
    char=ord("g"), color=(63, 127, 63), name="Goblin", blocks_movement=True
)

orc = entity.Entity(
    char=ord("o"), color=(63, 127, 63), name="Orc", blocks_movement=True
)
