import subprocess
from typing import Dict, List, Optional
from controllers.ScreenController import ScreenController
from dao.ScreenSlot import ScreenSlot
from controllers.ScreenSlotController import ScreenSlotController
from dao.TwitchWindow import TwitchWindow
from dao.ScreenCorner import ScreenCorner
from dao.Screen import Screen
import logging

class TwitchWindowController:

    SCREEN_CONTROLLER = ScreenController()
    SCREEN_SLOT_CONTROLLER = ScreenSlotController()

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def create_twitch_windows(self) -> List[TwitchWindow]:
        self.logger.debug("Creating Twitch windows.")
        result = subprocess.run(['wmctrl', '-lG'], capture_output=True, text=True)
        windows = result.stdout.splitlines()
        twitch_windows: List[TwitchWindow] = []
        for window in windows:
            if "Twitch" in window:
                twitch_window = TwitchWindow.from_wmctrl_output(window)
                twitch_windows.append(twitch_window)
        self.logger.debug(f"Created Twitch windows: {twitch_windows}")
        return twitch_windows

    def arrange_windows(self) -> None:
        self.logger.debug("Starting to arrange windows.")
        screens: List[Screen] = self.SCREEN_CONTROLLER.create_screen()
        self.logger.debug(f"Created screens: {screens}")
        twitch_windows: List[TwitchWindow] = self.create_twitch_windows()
        self.logger.debug(f"Found Twitch windows: {twitch_windows}")
        screen_slots: List[ScreenSlot] = self.SCREEN_SLOT_CONTROLLER.create_screen_slots(screens)
        self.logger.debug(f"Created screen slots: {screen_slots}")
        self.SCREEN_SLOT_CONTROLLER.assign_windows_to_slots(twitch_windows, screen_slots)
        # for slot in screen_slots:
        #     slot.fit_window()
        self.logger.debug("Assigned windows to slots.")