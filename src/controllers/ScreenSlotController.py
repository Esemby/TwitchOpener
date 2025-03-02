from typing import Dict, List, Tuple
import logging

from dao.Screen import Screen
from dao.ScreenCorner import ScreenCorner
from dao.ScreenSlot import ScreenSlot
from dao.TwitchWindow import TwitchWindow


class ScreenSlotController:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def is_window_in_slot(self, window: TwitchWindow, slot: ScreenSlot) -> bool:
        x, y = window.get_position()
        slot_x, slot_y = slot.get_position()
        slot_width, slot_height = slot.get_size()

        if slot.get_screen().is_sixteen_by_nine:
            if slot.get_screen_corner() == ScreenCorner.TOP_LEFT:
                return x < slot_x + slot_width // 2 and y < slot_y + slot_height // 2
            if slot.get_screen_corner() == ScreenCorner.TOP_RIGHT:
                return x > slot_x + slot_width // 2 and y < slot_y + slot_height // 2
            if slot.get_screen_corner() == ScreenCorner.BOTTOM_LEFT:
                return x < slot_x + slot_width // 2 and y > slot_y + slot_height // 2
            if slot.get_screen_corner() == ScreenCorner.BOTTOM_RIGHT:
                return x > slot_x + slot_width // 2 and y > slot_y + slot_height // 2
        elif slot.get_screen().is_nine_by_sixteen:
            if slot.get_screen_corner() == ScreenCorner.TOP:
                return y < slot_y + slot_height // 2
            if slot.get_screen_corner() == ScreenCorner.BOTTOM:
                return y > slot_y + slot_height // 2
        else:
            return x >= slot_x and x < slot_x + slot_width and y >= slot_y and y < slot_y + slot_height

    def get_fullscreen_slot(self, screen_slots: List[ScreenSlot]) -> ScreenSlot:
        return next((slot for slot in screen_slots if slot.is_fullscreen()), None)
    
    def get_slots_by_screen(self, screen_slots: List[ScreenSlot], screen: Screen) -> List[ScreenSlot]:
        return [slot for slot in screen_slots if slot.get_screen() == screen]

    def create_screen_slots(self, screens: List[Screen]) -> List[ScreenSlot]:
        self.logger.debug("Creating screen slots.")
        screen_slots: List[ScreenSlot] = []
        for screen in screens:
            if screen.is_sixteen_by_nine():
                screen_slots.append(ScreenSlot(screen, ScreenCorner.TOP_LEFT))
                screen_slots.append(ScreenSlot(screen, ScreenCorner.TOP_RIGHT))
                screen_slots.append(ScreenSlot(screen, ScreenCorner.BOTTOM_LEFT))
                screen_slots.append(ScreenSlot(screen, ScreenCorner.BOTTOM_RIGHT))
            if screen.is_nine_by_sixteen():
                screen_slots.append(ScreenSlot(screen, ScreenCorner.TOP))
                screen_slots.append(ScreenSlot(screen, ScreenCorner.BOTTOM))
            screen_slots.append(ScreenSlot(screen, ScreenCorner.FULLSCREEN))
        self.logger.debug(f"Created screen slots: {screen_slots}")
        return screen_slots

    def get_free_slots(self, screen_slots: List[ScreenSlot]) -> List[ScreenSlot]:  # Added type hints
        return [slot for slot in screen_slots if slot.is_free()]

    def assign_windows_to_slots(self, windows: List[TwitchWindow], slots: List[ScreenSlot]) -> None:
        self.logger.debug("Assigning windows to slots.")
        unassigned_windows: List[TwitchWindow] = []
        for window in windows:
            assigned = False
            for slot in slots:
                slot_cluster = self.get_slots_by_screen(slots, slot.get_screen())
                full_screen_slot = self.get_fullscreen_slot(slot_cluster)
                if self.can_screen_slot_be_used(window, slot, full_screen_slot):
                    slot.set_window(window)
                    assigned = True
                    break
            if not assigned:
                unassigned_windows.append(window)
        if unassigned_windows:
            free_slots = self.get_free_slots(slots)
            for window in unassigned_windows:
                if not free_slots:
                    break
                free_slot: ScreenSlot = free_slots.pop(0)
                free_slot.set_window(window)
        self.logger.debug("Assigned windows to slots.")

    def can_screen_slot_be_used(self, window: TwitchWindow, slot: ScreenSlot, full_screen_slot: ScreenSlot) -> bool:
        return slot.is_free() and self.is_window_in_slot(window, slot) and (slot == full_screen_slot or full_screen_slot.is_free())
