import subprocess
from typing import List, Optional
from TwitchWindow import TwitchWindow
from ScreenCorner import ScreenCorner
from Screen import Screen

class TwitchWindowController:
    def __init__(self):
        # Initialize any necessary attributes
        pass

    def get_twitch_windows(self) -> List[str]:        
        result = subprocess.run(['wmctrl', '-lG'], capture_output=True, text=True)
        windows = result.stdout.splitlines()
        twitch_windows = []
        for window in windows:
            if "Twitch" in window:
                twitch_window = TwitchWindow.from_wmctrl_output(window)
                twitch_windows.append(twitch_window)
        return twitch_windows

    def arrange_windows(self) -> None:
        twitch_windows = self.get_twitch_windows()
        # check position of every twitch window
        # make sure they are properly arranged in their corner
        # if a window find another window in its corner, move it to the next corner
        # we go from screen to screen, top left, top right, bottom left, bottom right
        pass

    def get_screens(self) -> List[Screen]:
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        screen_lines = [line for line in result.stdout.splitlines() if ' connected ' in line]
        screens = []
        for line in screen_lines:
            screen = Screen.from_xrandr_output(line)
            if screen:
                screens.append(screen)
        return screens
    


    @staticmethod
    def determine_screen_corner(window: TwitchWindow, screen: Screen ) -> Optional[ScreenCorner]:
        screen_info = self.get_screen_info()
        screen_number = screen.get_screen_number()
        if screen_number is not None:
            screen_width, screen_height, screen_x, screen_y = screen_info[screen_number]
            x, y = self.get_position()
            width, height = self.get_size()
            # Fullscreen
            if width == screen_width and height == screen_height:  
                return ScreenCorner.FULLSCREEN
            # Vertical screen
            if screen_height > screen_width:  
                if y < screen_y + screen_height // 2:
                    return ScreenCorner.TOP
                else:
                    return ScreenCorner.BOTTOM
            # Corners
            if x < screen_x + screen_width // 2 and y < screen_y + screen_height // 2:
                return ScreenCorner.TOP_LEFT
            elif x >= screen_x + screen_width // 2 and y < screen_y + screen_height // 2:
                return ScreenCorner.TOP_RIGHT
            elif x < screen_x + screen_width // 2 and y >= screen_y + screen_height // 2:
                return ScreenCorner.BOTTOM_LEFT
            else:
                return ScreenCorner.BOTTOM_RIGHT
        return None