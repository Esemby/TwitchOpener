import subprocess
from typing import List
from dao.Screen import Screen
import logging

class ScreenController:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def create_screen(self) -> List[Screen]:
        self.logger.debug("Creating screens.")
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        screen_lines = [line for line in result.stdout.splitlines() if ' connected ' in line]
        screens: List[Screen] = []
        for line in screen_lines:
            screen = Screen.from_xrandr_output(line)
            if screen:
                screens.append(screen)
        self.logger.debug(f"Created screens: {screens}")
        return screens
