import unittest

from htmlnode import HTMLNode


class HtmlTextNode(unittest.TestCase):
    def test_neq(self):
        node = HTMLNode(
            "a", "Link", children=None, props={"href": "https://www.boot.dev"}
        )
        node2 = HTMLNode(
            "a", "Link", children=None, props={"href": "https://examples.dev"}
        )
        # print(node.__repr__())
        # print(node2.__repr__())

        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
