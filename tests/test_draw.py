import sys, os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualizer.draw import draw

class TestDraw(unittest.TestCase):
    def test_draw_graph(self):
        edges = [(0, 1, 4), (1, 2, 2), (2, 3, 3), (3, 0, 1)]
        draw(4, edges, directed=False, filename="test_graph_out.png", highlight=[(0, 1)], show=False)

if __name__ == "__main__":
    unittest.main()