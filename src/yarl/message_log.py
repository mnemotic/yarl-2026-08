import textwrap
from collections.abc import Iterable, Reversible

from tcod.console import Console

from yarl import colors


class Message:
    def __init__(self, text: str, fg: tuple[int, int, int]):
        self.fg = fg
        self.text = text
        self.count = 1

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text


class MessageLog:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def append(
        self, text: str, fg: tuple[int, int, int] = colors.WHITE, *, stack: bool = True
    ) -> None:
        if stack and len(self.messages) > 0 and text == self.messages[-1].text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def print(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        self.print_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        """Return a wrapped string."""
        for line in string.splitlines():
            yield from textwrap.wrap(line, width, expand_tabs=True)

    @classmethod
    def print_messages(
        cls,
        console: Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        y_offset = 0
        for message in reversed(messages):
            for line in list(cls.wrap(str(message), width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset += 1
                if y_offset >= height:
                    return
