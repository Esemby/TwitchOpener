import unittest
import sys
import os

# Ensure the correct path is added
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from src.Screen import Screen

class TestScreen(unittest.TestCase):
    def test_getters(self):
        screen = Screen()
        screen.set_get_name(lambda: "Screen1")
        screen.set_get_x(lambda: 100)
        screen.set_get_y(lambda: 200)
        screen.set_get_width(lambda: 1920)
        screen.set_get_height(lambda: 1080)

        self.assertEqual(screen.get_name(), "Screen1")
        self.assertEqual(screen.get_x(), 100)
        self.assertEqual(screen.get_y(), 200)
        self.assertEqual(screen.get_width(), 1920)
        self.assertEqual(screen.get_height(), 1080)
        self.assertEqual(screen.get_position(), (100, 200))
        self.assertEqual(screen.get_size(), (1920, 1080))

    def test_from_xrandr_output(self):
        output = "Screen1 connected primary 1920x1080+100+200"
        screen = Screen.from_xrandr_output(output)
        
        self.assertIsNotNone(screen)
        self.assertEqual(screen.get_name(), "Screen1")
        self.assertEqual(screen.get_x(), 100)
        self.assertEqual(screen.get_y(), 200)
        self.assertEqual(screen.get_width(), 1920)
        self.assertEqual(screen.get_height(), 1080)

if __name__ == '__main__':
    unittest.main()
