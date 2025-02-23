import subprocess
from typing import List, Optional, Tuple
from TwitchWindow import TwitchWindow
from TwitchWindowController import TwitchWindowController

twitch_window_controller = TwitchWindowController()

def list_windows_with_positions() -> List[str]:
    result = subprocess.run(['wmctrl', '-lG'], capture_output=True, text=True)
    windows = result.stdout.splitlines()
    for window in windows:
        parts = window.split()
        window_id = parts[0]
        desktop_id = parts[1]
        x = parts[2]
        y = parts[3]
        width = parts[4]
        height = parts[5]
        title = ' '.join(parts[6:])
        print(f"Window: {title}, Position: ({x}, {y}), Size: ({width}, {height})")
    return windows

def get_screen_info(screen_number: int) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
    result = subprocess.run(['xrandr'], capture_output=True, text=True)
    screens = [line for line in result.stdout.splitlines() if ' connected ' in line]
    if screen_number < len(screens):
        screen_info = screens[screen_number].split()
        dimensions = screen_info[2] if 'primary' not in screen_info else screen_info[3]
        position = dimensions.split('+')[1:]
        dimensions = dimensions.split('+')[0]
        screen_width, screen_height = [int(dim) for dim in dimensions.split('x')]
        screen_x, screen_y = [int(pos) for pos in position]
        print(f"Screen {screen_number} dimensions: {screen_width}x{screen_height}, position: {screen_x},{screen_y}")
        return screen_width, screen_height, screen_x, screen_y
    return None, None, None, None

def arrange_twitch_windows(twitch_windows: List[TwitchWindow]) -> None:
    for twitch_window in twitch_windows:
        screen_number = twitch_window.get_screen()
        if screen_number is not None:
            screen_width, screen_height, screen_x, screen_y = get_screen_info(screen_number)
            positions = [
                (screen_x, screen_y, screen_width // 2, screen_height // 2),  # Top-left corner
                (screen_x + screen_width // 2, screen_y, screen_width // 2, screen_height // 2),  # Top-right corner
                (screen_x, screen_y + screen_height // 2, screen_width // 2, screen_height // 2),  # Bottom-left corner
                (screen_x + screen_width // 2, screen_y + screen_height // 2, screen_width // 2, screen_height // 2)  # Bottom-right corner
            ]
            x, y, w, h = positions[twitch_windows.index(twitch_window) % len(positions)]
            subprocess.run(['wmctrl', '-ir', twitch_window.get_window_id, '-e', f'0,{x},{y},{w},{h}'])

def list_all_screens() -> None:
    result = subprocess.run(['xrandr'], capture_output=True, text=True)
    screens = [line for line in result.stdout.splitlines() if ' connected ' in line]
    for i, screen in enumerate(screens):
        screen_info = screen.split()
        dimensions = screen_info[2] if 'primary' not in screen_info else screen_info[3]
        dimensions = dimensions.split('+')[0]
        position = dimensions.split('+')[1:]
        screen_width, screen_height = [int(dim) for dim in dimensions.split('x')]
        screen_x, screen_y = [int(pos) for pos in position]
        print(f"Screen {i}: dimensions: {screen_width}x{screen_height}, position: {screen_x},{screen_y}")

if __name__ == "__main__":
    twitch_windows = twitch_window_controller.get_twitch_windows()
    arrange_twitch_windows(twitch_windows)