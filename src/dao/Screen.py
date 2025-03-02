import re
from typing import Callable, Optional, Tuple

class Screen:
    def __init__(self):
        self._get_number: Optional[Callable[[], int]] = None
        self._get_name: Optional[Callable[[], str]] = None
        self._get_x: Optional[Callable[[], int]] = None
        self._get_y: Optional[Callable[[], int]] = None
        self._get_width: Optional[Callable[[], int]] = None
        self._get_height: Optional[Callable[[], int]] = None

    def set_get_number(self, number_getter: Callable[[], int]):
        self._get_number = number_getter

    def get_number(self) -> int:
        return self._get_number()

    def set_get_name(self, name_getter: Callable[[], str]):
        self._get_name = name_getter

    def get_name(self) -> str:
        return self._get_name()

    def set_get_x(self, x_getter: Callable[[], int]):
        self._get_x = x_getter

    def get_x(self) -> int:
        return self._get_x()

    def set_get_y(self, y_getter: Callable[[], int]):
        self._get_y = y_getter

    def get_y(self) -> int:
        return self._get_y()

    def set_get_width(self, width_getter: Callable[[], int]):
        self._get_width = width_getter

    def get_width(self) -> int:
        return self._get_width()

    def set_get_height(self, height_getter: Callable[[], int]):
        self._get_height = height_getter

    def get_height(self) -> int:
        return self._get_height()

    def get_position(self) -> Tuple[int, int]:
        return self.get_x(), self.get_y()

    def get_size(self) -> Tuple[int, int]:
        return self.get_width(), self.get_height()
    
    def is_sixteen_by_nine(self) -> bool:
        return self.get_width() / self.get_height() == 16 / 9
    
    def is_nine_by_sixteen(self) -> bool:
        return self.get_width() / self.get_height() == 9 / 16

    @staticmethod
    def from_xrandr_output(output: str) -> 'Screen':
        match = re.search(r'(\S+) connected.*?(\d+)x(\d+)\+(\d+)\+(\d+)', output)
        if match:
            screen = Screen()
            screen.set_get_name(lambda: match.group(1))
            screen.set_get_width(lambda: int(match.group(2)))
            screen.set_get_height(lambda: int(match.group(3)))
            screen.set_get_x(lambda: int(match.group(4)))
            screen.set_get_y(lambda: int(match.group(5)))
            return screen
        return None