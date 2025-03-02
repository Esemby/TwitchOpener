import logging
import subprocess
from dao.Screen import Screen
from dao.ScreenCorner import ScreenCorner
from dao.TwitchWindow import TwitchWindow

class ScreenSlot:
    
    RIGHT_SIDED_SLOTS = [ScreenCorner.TOP_RIGHT, ScreenCorner.BOTTOM_RIGHT]
    BOTTOM_SIDED_SLOTS = [ScreenCorner.BOTTOM_LEFT, ScreenCorner.BOTTOM_RIGHT]
    NON_QUARTER_SLOTS = [ScreenCorner.FULLSCREEN, ScreenCorner.TOP, ScreenCorner.MIDDLE, ScreenCorner.BOTTOM]

    def __init__(self, screen: Screen, screen_corner: ScreenCorner, window: TwitchWindow = None):
        self._screen = screen
        self._screen_corner = screen_corner
        self._window = window

    def get_screen(self) -> Screen:
        return self._screen

    def set_screen(self, screen: Screen):
        self._screen = screen

    def get_screen_corner(self) -> ScreenCorner:
        return self._screen_corner

    def set_screen_corner(self, screen_corner: ScreenCorner):
        self._screen_corner = screen_corner

    def get_x(self) -> int:
        if self._screen_corner in self.RIGHT_SIDED_SLOTS:
            return self._screen.get_x() + self._screen.get_width() // 2
        else:
            return self._screen.get_x()
        
    def get_y(self) -> int:
        if self._screen_corner in self.BOTTOM_SIDED_SLOTS:
            return self._screen.get_y() + self._screen.get_height() // 2
        else:
            return self._screen.get_y()
        
    def get_position(self) -> tuple:
        return (self.get_x(), self.get_y())
        
    def get_width(self) -> int:
        width : int = self._screen.get_width() 
        if self._screen_corner not in self.NON_QUARTER_SLOTS:
            width //= 2
        return width + 25
    
    def get_height(self) -> int:
        height : int = self._screen.get_height()
        if self._screen_corner != ScreenCorner.FULLSCREEN:
            height //= 2
        return height + 50

    def get_size(self) -> tuple:
        return (self.get_width(), self.get_height())

    def get_window(self) -> TwitchWindow:
        return self._window
    
    def set_window(self, window: TwitchWindow):
        self._window = window

    def is_free(self) -> bool:
        return self._window is None
    
    def is_fullscreen(self) -> bool:
        return self._screen_corner == ScreenCorner.FULLSCREEN
    
    def fit_window(self):
        if self._window:
            logging.debug(f"Fitting window {self._window.get_title()} to slot with values: x={self.get_x()}, y={self.get_y()}, width={self.get_width()}, height={self.get_height()}")
            subprocess.run(['wmctrl', '-ir', self._window.get_window_id(), '-e', f'0,{self.get_x()},{self.get_y()},{self.get_width()},{self.get_height()}'])