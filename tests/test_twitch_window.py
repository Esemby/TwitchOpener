import unittest
import sys
import os

# Ensure the correct path is added
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from src.TwitchWindow import TwitchWindow

class TestTwitchWindow(unittest.TestCase):
    def test_getters(self):
        twitch_window = TwitchWindow()
        twitch_window.set_get_window_id(lambda: "0x12345")
        twitch_window.set_get_title(lambda: "Twitch Stream")
        twitch_window.set_get_x(lambda: 300)
        twitch_window.set_get_y(lambda: 400)
        twitch_window.set_get_width(lambda: 1280)
        twitch_window.set_get_height(lambda: 720)

        self.assertEqual(twitch_window.get_window_id(), "0x12345")
        self.assertEqual(twitch_window.get_title(), "Twitch Stream")
        self.assertEqual(twitch_window.get_x(), 300)
        self.assertEqual(twitch_window.get_y(), 400)
        self.assertEqual(twitch_window.get_width(), 1280)
        self.assertEqual(twitch_window.get_height(), 720)
        self.assertEqual(twitch_window.get_position(), (300, 400))
        self.assertEqual(twitch_window.get_size(), (1280, 720))

    def test_from_wmctrl_output(self):
        output = "0x12345  0 300 400 1280 720 Twitch Stream"
        twitch_window = TwitchWindow.from_wmctrl_output(output)
        
        self.assertIsNotNone(twitch_window)
        self.assertEqual(twitch_window.get_window_id(), "0x12345")
        self.assertEqual(twitch_window.get_title(), "Twitch Stream")
        self.assertEqual(twitch_window.get_x(), 300)
        self.assertEqual(twitch_window.get_y(), 400)
        self.assertEqual(twitch_window.get_width(), 1280)
        self.assertEqual(twitch_window.get_height(), 720)

if __name__ == '__main__':
    unittest.main()
