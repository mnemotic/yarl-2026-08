class Entity:
    """Generic game object representing player chareacters, NPCs, items, etc."""

    x: int
    y: int
    char: int
    color: tuple[int, int, int]

    def __init__(self, x: int, y: int, char: int, color: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
