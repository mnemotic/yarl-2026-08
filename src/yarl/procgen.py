import random
from collections.abc import Iterator

import tcod

import yarl.engine
import yarl.entity_factories
import yarl.tile_types as tiles
from yarl import game_map


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x0 = x
        self.y0 = y
        self.x1 = x + width
        self.y1 = y + height

    @property
    def center(self) -> tuple[int, int]:
        x = (self.x0 + self.x1) // 2
        y = (self.y0 + self.y1) // 2
        return x, y

    @property
    def interior(self) -> tuple[slice, slice]:
        """Returns the inner area of this room as a 2D array index."""
        return slice(self.x0 + 1, self.x1), slice(self.y0 + 1, self.y1)

    def intersects(self, other: RectangularRoom) -> bool:
        """Returns `True` if this room overlaps with another `RectangularRoom`."""
        return (
            self.x0 <= other.x1
            and self.x1 >= other.x0
            and self.y0 <= other.y1
            and self.y1 >= other.y0
        )


def make_tunnel(
    start: tuple[int, int],
    end: tuple[int, int],
) -> Iterator[tuple[int, int]]:
    x0, y0 = start
    x1, y1 = end
    if random.random() < 0.5:
        corner_x, corner_y = x1, y0
    else:
        corner_x, corner_y = x0, y1

    yield from tcod.los.bresenham((x0, y0), (corner_x, corner_y)).tolist()
    yield from tcod.los.bresenham((corner_x, corner_y), (x1, y1)).tolist()


def generate_dungeon(
    *,
    map_width: int,
    map_height: int,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    max_monsters_per_room: int,
    engine: yarl.engine.Engine,
) -> game_map.GameMap:
    player = engine.player
    dungeon = game_map.GameMap(engine, map_width, map_height, entities=[player])

    rooms: list[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        room = RectangularRoom(x, y, room_width, room_height)
        if any(room.intersects(other) for other in rooms):
            continue

        dungeon.tiles[room.interior] = tiles.floor

        if len(rooms) == 0:
            player.place(*room.center, dungeon)
        else:
            for x, y in make_tunnel(rooms[-1].center, room.center):
                dungeon.tiles[x, y] = tiles.floor
            # Monsters are not places in the starting room.
            place_entities(room, dungeon, max_monsters_per_room)

        rooms.append(room)

    return dungeon


def place_entities(
    room: RectangularRoom, dungeon: game_map.GameMap, max_entities: int
) -> None:
    num_entities = random.randint(0, max_entities)

    for i in range(num_entities):
        x = random.randint(room.x0 + 1, room.x1 - 1)
        y = random.randint(room.y0 + 1, room.y1 - 1)

        if not any(e.x == x and e.y == y for e in dungeon.entities):
            if random.random() < 0.8:
                yarl.entity_factories.goblin.spawn(dungeon, x, y)
            else:
                yarl.entity_factories.orc.spawn(dungeon, x, y)
