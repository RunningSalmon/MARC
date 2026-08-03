from enum import Enum
import re

Printing_Colors = {
    0: "\033[48;2;0;0;0m",  # Black (background)
    1: "\033[48;2;0;116;217m",  # Blue
    2: "\033[48;2;255;65;54m",  # Red
    3: "\033[48;2;46;204;64m",  # Green
    4: "\033[48;2;255;220;0m",  # Yellow
    5: "\033[48;2;170;170;170m",  # Grey
    6: "\033[48;2;240;18;190m",  # Pink
    7: "\033[48;2;255;133;27m",  # Orange
    8: "\033[48;2;127;219;255m",  # Azure
    9: "\033[48;2;135;12;37m",  # Maroon
    10: "\033[0m"  # Reset Color Printing
}


class ArcColor(Enum):
    Black = 0
    Blue = 1
    Red = 2
    Green = 3
    Yellow = 4
    Grey = 5
    Fuchsia = 6
    Orange = 7
    Azure = 8
    Maroon = 9

    def to_hex(self) -> str:
        """Converts the Ansi color to a hex string."""
        match = re.search(r'(\d+);(\d+);(\d+)m$', Printing_Colors[self.value])
        r, g, b = (int(x) for x in match.groups())
        return f'#{r:02x}{g:02x}{b:02x}'


class Direction(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3


class Axis(Enum):
    Horizontal = 0
    Vertical = 1


class Degree(Enum):
    Deg90 = -1
    Deg180 = -2
    Deg270 = -3


class SmallerOrLarger(Enum):
    smaller = 0
    larger = 1
