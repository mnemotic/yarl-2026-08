class Entity:
    """Generic game object representing player chareacters, NPCs, items, etc."""

    def __init__(self, x: int, y: int, char: int, color: tuple[int, int, int]):
        self.x: int = x
        self.y: int = y
        self.char: int = char
        self.color: tuple[int, int, int] = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
