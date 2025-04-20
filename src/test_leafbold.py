import unittest
from leafnode import LeafNode


class LeafTest(unittest.TestCase):
    def test_leaf_to_html_b(self):
        node = LeafNode(value="Hello, world!")
        # print(node.to_html())
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
