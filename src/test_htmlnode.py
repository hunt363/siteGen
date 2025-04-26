import unittest

from htmlnode import HTMLNode


class HtmlTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("b", "Hello")
        node2 = HTMLNode("b", "Hello")
        # print(node.__repr__())
        # print(node2.__repr__())
        self.assertEqual(node, node2)

    def test_eq(self):
        node = HTMLNode(
            "a", "Link", children=[HTMLNode("<th>"), HTMLNode("<tr>")], props=None
        )
        node2 = HTMLNode(
            "a", "Link", children=[HTMLNode("<th>"), HTMLNode("<tr>")], props=None
        )
        # print(node.__repr__())
        # print(node2.__repr__())

        self.assertEqual(node, node2)

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
