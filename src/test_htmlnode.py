import unittest

from htmlnode import HTMLNode


class HtmlTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("b", "Hello")
        node2 = HTMLNode("b", "Hello")
        # print(node.__repr__())
        # print(node2.__repr__())
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
