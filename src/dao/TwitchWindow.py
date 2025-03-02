from typing import Optional, Callable

class TwitchWindow:
    def __init__(self):
        self._get_window_id: Optional[Callable[[], str]] = None
        self._get_title: Optional[Callable[[], str]] = None
        self._get_x: Optional[Callable[[], int]] = None
        self._get_y: Optional[Callable[[], int]] = None
        self._get_width: Optional[Callable[[], int]] = None
        self._get_height: Optional[Callable[[], int]] = None

    def set_get_window_id(self, func: Callable[[], str]):
        self._get_window_id = func

    def set_get_title(self, func: Callable[[], str]):
        self._get_title = func

    def set_get_x(self, func: Callable[[], int]):
        self._get_x = func

    def set_get_y(self, func: Callable[[], int]):
        self._get_y = func

    def set_get_width(self, func: Callable[[], int]):
        self._get_width = func

    def set_get_height(self, func: Callable[[], int]):
        self._get_height = func

    def get_window_id(self) -> str:
        return self._get_window_id()

    def get_title(self) -> str:
        return self._get_title()

    def get_x(self) -> int:
        return self._get_x()

    def get_y(self) -> int:
        return self._get_y()

    def get_width(self) -> int:
        return self._get_width()

    def get_height(self) -> int:
        return self._get_height()

    def get_position(self) -> tuple:
        return (self.get_x(), self.get_y())

    def get_size(self) -> tuple:
        return (self.get_width(), self.get_height())

    @classmethod
    def from_wmctrl_output(cls, output: str):
        parts = output.split()
        window_id = parts[0]
        x = int(parts[2])
        y = int(parts[3])
        width = int(parts[4])
        height = int(parts[5])
        title = " ".join(parts[6:])
        
        twitch_window = cls()
        twitch_window.set_get_window_id(lambda: window_id)
        twitch_window.set_get_title(lambda: title)
        twitch_window.set_get_x(lambda: x)
        twitch_window.set_get_y(lambda: y)
        twitch_window.set_get_width(lambda: width)
        twitch_window.set_get_height(lambda: height)
        
        return twitch_window
